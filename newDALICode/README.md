## PR
`youtube-dl` tool is outdated. YouTube frequently updates its player code, and older versions of youtube-dl may fail to extract video signatures.

The error occured when we use `get_audio` to download the audio.

if we use 
```python
path_audio = os.path.abspath('dataset/DALI/audio')

dali_info = dali_code.get_info(dali_data_path + '/info/DALI_DATA_INFO.gz')

# Get Audio
errors = dali_code.get_audio(dali_info, path_audio, skip=[], keep=[])
```
We may receive the error like:
```bash
youtube_dl.utils.ExtractorError: Could not find JS function 'decodeURIComponent'; please report this issue on https://yt-dl.org/bug . Make sure you are using the latest version; see  https://yt-dl.org/update  on how to update. Be sure to call youtube-dl with the --verbose flag and include its complete output.
```
