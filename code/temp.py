# # Lyrics Line Type for Walaoke extension of LRC
# class LyricsLineType(Enum):
#     N = 0 # Normal Line
#     M = 1 # Male
#     F = 2 # Female
#     D = 3 # Duet


# # Word-Synced Lyrics Segments
# @dataclass
# class LyricsSegment_WS:
#     label: str
#     start: float
#     end: float
#     duration: float
#     endOfLine: bool


# # Word-Synced Lyrics Line
# class LyricsLine_WS:
#     def __init__(self):
#         self.lyricsWords = []
#         self.wordCounts = 0
#         self.start = 0.0
#         self.end = 0.0
#         self.duration = 0.0
#         self.type = LyricsLineType.N

#     def add_segment(self, label: str, start: float, end: float, endOfLine: bool):
#         self.lyricsWords.append(LyricsSegment_WS(label=label, start=start, end=end, duration=end-start, endOfLine=endOfLine))
#         self.wordCounts += 1
#         self.duration += end - start
#         self.end = end
#         if len(self.lyricsWords) == 1:
#             self.start = start


# # Word-Synced Lyrics
# class Lyrics_WS:
#     def __init__(self):
#         self.lyricsWords = []
#         self.lyricsLines = []
#         self.wordCounts = 0
#         self.duration = 0.0
#         self.title = ''
#         self.artist = ''
#         self.album = ''

#     def add_segment(self, label: str, start: float, end: float, endOfLine: bool):
#         self.lyricsWords.append(LyricsSegment_WS(label=label, start=start, end=end, duration=end-start, endOfLine=endOfLine))
#         self.wordCounts += 1