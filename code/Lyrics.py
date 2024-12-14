from dataclasses import dataclass


# Word-Synced Lyrics Segments
@dataclass
class LyricsSegment_WS:
    label: str
    start: float
    end: float
    duration: float

# Word-Synced Lyrics
class Lyrics_WS:
    def __init__(self):
        self.lyrics = []
        self.wordCounts = 0
        self.duration = 0.0

    def add_segment(self, label: str, start: float, end: float):
        self.lyrics.append(LyricsSegment_WS(label=label, start=start, end=end, duration=end-start))
        self.wordCounts += 1

# class Lyrics():
