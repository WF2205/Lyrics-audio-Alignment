import DALI as dali_code
import os

# References : https://github.com/gabolsgabs/DALI
dali_data_path = os.path.abspath('dataset/DALI/v1/data')
path_audio = os.path.abspath('dataset/DALI/audio')

dali_data = dali_code.get_the_DALI_dataset(dali_data_path, skip=[], keep=[])
dali_info = dali_code.get_info(dali_data_path + '/info/DALI_DATA_INFO.gz')

# Get Audio
downloaded_audio = [os.path.splitext(x)[0] for x in os.listdir(path_audio)]
errors = dali_code.get_audio(dali_info, path_audio, skip=downloaded_audio, keep=[])
# errors -> ['dali_id', 'youtube_url', 'error']