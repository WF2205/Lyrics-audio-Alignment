# Library
import torch
import torchaudio
import torchaudio.functional as F
from Lyrics import Lyrics_WS

ORIGINAL_SR = 44100
TARGET_SR = 16000

# Return pytorch device
def select_device(mps_enable = True):
    if torch.cuda.is_available():
        return torch.device('cuda')     # CUDA
    elif torch.backends.mps.is_available() & mps_enable: 
        return torch.device('mps')    # Apple Sillicon
    else:
        return torch.device("cpu")    # CPU

def unflatten(list_, lengths):
    assert len(list_) == sum(lengths)
    i = 0
    ret = []
    for l in lengths:
        ret.append(list_[i : i + l])
        i += l
    return ret

def align(emission, tokens, device):
    targets = torch.tensor([tokens], dtype=torch.int32, device=device)
    alignments, scores = F.forced_align(emission, targets, blank=0)

    alignments, scores = alignments[0], scores[0]  # remove batch dimension for simplicity
    scores = scores.exp()  # convert back to probability
    return alignments, scores

# Compute average score weighted by the span length
def _score(spans):
    return sum(s.score * len(s) for s in spans) / sum(len(s) for s in spans)



def MMS_pytorch_sync(audio_path, lyrics_words_path):
    # Select Device
    device = select_device(False)
    # print("[MMS_pytorch_sync] Device Selected:", device)
    
    # Generate emissions
    waveform, _ = torchaudio.load(audio_path)
    bundle = torchaudio.pipelines.MMS_FA
    model = bundle.get_model(with_star=False).to(device)
    with torch.inference_mode():
        emission, _ = model(waveform.to(device))
    
    # Load Lyrics
    with open(lyrics_words_path, "r") as file:
        lines = file.readlines()
    # Remove the newline characters (optional)
    TRANSCRIPT = [line.strip() for line in lines]

    # Tokenize the transcript
    LABELS = bundle.get_labels(star=None)
    DICTIONARY = bundle.get_dict(star=None)
    tokenized_transcript = [DICTIONARY[c] for word in TRANSCRIPT for c in word]

    # Alignments
    aligned_tokens, alignment_scores = align(emission, tokenized_transcript, device)
    token_spans = F.merge_tokens(aligned_tokens, alignment_scores)
    word_spans = unflatten(token_spans, [len(word) for word in TRANSCRIPT])

    num_frames = emission.size(1)
    sample_rate=bundle.sample_rate
    synced_lyrics = Lyrics_WS()
    for i in range(len(word_spans)):
        ratio = waveform.size(1) / num_frames
        x0 = int(ratio * word_spans[i][0].start)
        x1 = int(ratio * word_spans[i][-1].end)
        synced_lyrics.add_segment(label=TRANSCRIPT[i], start=x0 / sample_rate, end=x1 / sample_rate)
        # print(f"{TRANSCRIPT[i]} ({_score(word_spans[i]):.2f}): {x0 / sample_rate:.3f} - {x1 / sample_rate:.3f} sec")
    
    return synced_lyrics



