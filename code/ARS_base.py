# Library
import torch
import demucs
import librosa
import soundfile
import transformers
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor, logging, Wav2Vec2CTCTokenizer, Wav2Vec2FeatureExtractor
from demucs.separate import load_track
from dataclasses import dataclass
from typing import List
from Lyrics import Lyrics_WS
from demucs.pretrained import get_model
from demucs.apply import apply_model


SEPARATOR = '|'



@dataclass
class Segment:
    label: str
    start: int
    end: int


@dataclass
class Point:
    token_index: int
    time_index: int
    prob: float


def seconds_to_lrc(seconds, is_word = True):
    minutes = int(seconds // 60)
    seconds = seconds % 60
    hundredths = int((seconds % 1) * 100)
    seconds = int(seconds)
    formated = f"{minutes:02d}:{seconds:02d}.{hundredths:02d}"
    return f"<{formated}>" if is_word else f"[{formated}]"


@dataclass
class Word:
    label: str
    start: float
    end: float

    def __repr__(self):
        return f"{seconds_to_lrc(self.start)} {self.label}"


class LrcFormatter():
    @staticmethod
    def words2lrc(words: List[Word], original_lyrics: str, lang="en-US"):
        lrc = ""
        counter = 0
        word_end = None
        for line in original_lyrics.splitlines():
            if line == '': continue
            if word_end:
                lrc += f"\n{seconds_to_lrc(word_end, False)}"
            else:
                lrc += "[00:00.00]"
            if lang == "en-US":
                splitted_words = line.split(' ')
            elif lang == "zh-CN":
                splitted_words = line

            for original_word in splitted_words:
                if original_word == '': continue
                word = words[counter]
                word.label = original_word
                lrc += f" {word}"
                word_end = word.end
                counter+=1
        return lrc


class Aligner():
    @staticmethod
    def align(emission, tokens, blank_id=0):
        trellis = Aligner.get_trellis(emission, tokens, blank_id=blank_id)
        path = Aligner.backtrack(trellis, emission, tokens, blank_id=blank_id)
        return path

    @staticmethod
    def get_trellis(emission, tokens, blank_id=0):
        num_frame = emission.size(0)
        num_tokens = len(tokens)
        trellis = torch.empty((num_frame + 1, num_tokens + 1))
        trellis[0, 0] = 0
        trellis[1:, 0] = torch.cumsum(emission[:, blank_id], 0)
        trellis[0, -num_tokens:] = -float("inf")
        trellis[-num_tokens:, 0] = float("inf")

        for t in range(num_frame):
            trellis[t + 1, 1:] = torch.maximum(
                # Score for staying at the same token
                trellis[t, 1:] + emission[t, blank_id],
                # Score for changing to the next token
                trellis[t, :-1] + emission[t, tokens],
            )
        return trellis

    @staticmethod
    def backtrack(trellis, emission, tokens, blank_id=0):
        j = trellis.size(1) - 1
        t_start = torch.argmax(trellis[:, j]).item()

        path = []
        for t in range(t_start, 0, -1):
            stayed = trellis[t - 1, j] + emission[t - 1, blank_id]
            changed = trellis[t - 1, j - 1] + emission[t - 1, tokens[j - 1]]
            prob = emission[t - 1, tokens[j - 1]
                            if changed > stayed else 0].exp().item()
            path.append(Point(j - 1, t - 1, prob))
            if changed > stayed:
                j -= 1
                if j == 0:
                    break
        else:
            raise Exception("Failed")
        return path[::-1]

    def get_words_from_path(text, path, frame_duration):
        # Skip repeating char
        i1, i2 = 0, 0
        segments = []
        while i1 < len(path):
            while i2 < len(path) and path[i1].token_index == path[i2].token_index:
                i2 += 1
            segments.append(
                Segment(
                    text[path[i1].token_index],
                    path[i1].time_index,
                    path[i2 - 1].time_index + 1
                )
            )
            i1 = i2
        # if lang == "en-US":
        return Aligner.merge_en(segments, frame_duration)
        # elif lang == "zh-CN":
        #     return [Word(s.label, s.start * frame_duration, s.end * frame_duration) for s in segments]
        

    def merge_en(segments, frame_duration, separator=SEPARATOR):
        # Merge chars to word
        words = []
        i1, i2 = 0, 0
        while i1 < len(segments):
            if i2 >= len(segments) or segments[i2].label == separator:
                if i1 != i2:
                    segs = segments[i1:i2]
                    word = "".join([seg.label for seg in segs])
                    words.append(Word(
                        word, segments[i1].start * frame_duration, segments[i2 - 1].end * frame_duration))
                i1 = i2 + 1
                i2 = i1
            else:
                i2 += 1
        return words

ORIGINAL_SR = 44100
TARGET_SR = 16000


def phoneme_recognizer(vocals, processor, model):
    vals = processor(vocals, return_tensors="pt", padding="longest", sampling_rate=16000).input_values
    duration_sec = vals.shape[1] / TARGET_SR
    with torch.no_grad():
        logits = model(vals).logits
    return logits.cpu().detach(), duration_sec


# Return pytorch device
def select_device(mps_enable = True):
    if torch.cuda.is_available():
        return torch.device('cuda')     # CUDA
    elif torch.backends.mps.is_available() & mps_enable: 
        return torch.device('mps')    # Apple Sillicon
    else:
        return torch.device("cpu")    # CPU

def ASR_sync(audio_path, lyrics_words_path):
    # Select Device
    device = select_device()

    # Load Lyrics
    with open(lyrics_words_path, "r") as file:
        lines = file.readlines()
    # Remove the newline characters (optional)
    lyrics_processed = [line.strip() for line in lines]
    lyrics_processed = '|'.join(lyrics_processed)
    lyrics_processed = lyrics_processed.upper()


    # Load Model
    model_id = 'facebook/wav2vec2-large-960h-lv60-self'
    Wav2Vec2_model = Wav2Vec2ForCTC.from_pretrained(model_id)
    Wav2Vec2_processor = Wav2Vec2Processor.from_pretrained(model_id)

    duration_sec = 0

    # Load Aduio Track
    audio_track, sr = librosa.load(audio_path, sr=ORIGINAL_SR)
    track_vocal = librosa.resample(audio_track, orig_sr=sr, target_sr=TARGET_SR)

    # Segmentation
    # Each column track_segments[:, i] contains a contiguous slice of the input track_vocal[i * hop_length : i * hop_length + frame_length]
    track_segments = librosa.util.frame(track_vocal, frame_length=int(TARGET_SR * 15), hop_length=int(TARGET_SR * 15), axis=0)

    # Get Raw Prediction
    # logits: the vector of raw (non-normalized) predictions
    duration_sec = 0
    logits, duration_temp = phoneme_recognizer(track_segments[0], Wav2Vec2_processor, Wav2Vec2_model)
    duration_sec += duration_temp
    for seg in track_segments[1:]:
        logits_seg, duration_temp = phoneme_recognizer(seg, Wav2Vec2_processor, Wav2Vec2_model)
        duration_sec += duration_temp
        # Concatenates the logits
        logits = torch.cat((logits, logits_seg), dim=1)

    # Normalize Results
    emission = torch.log_softmax(logits, dim=-1)[0].cpu().detach()

    # Get Prediction Results
    pred = torch.argmax(logits, dim=-1)
    transcription = Wav2Vec2_processor.batch_decode(pred)

    # Prepares text labels for the CTC
    lyrics_tokens = Wav2Vec2_processor.tokenizer(lyrics_processed).input_ids

    path = Aligner.align(emission, lyrics_tokens)

    words = Aligner.get_words_from_path(
                text=lyrics_processed, path=path, frame_duration=Wav2Vec2_model.config.inputs_to_logits_ratio / TARGET_SR)
    synced_lyrics = Lyrics_WS()
    for i in range(len(words)):
        synced_lyrics.add_segment(label=words[i].label, start=words[i].start, end=words[i].end)

    return synced_lyrics
