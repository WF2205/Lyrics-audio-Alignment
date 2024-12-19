from . import utilities as ut
import os
# import youtube_dl
import yt_dlp
import re

base_url = 'http://www.youtube.com/watch?v='


class MyLogger(object):
    def debug(self, msg):
        print(msg)

    def warning(self, msg):
        print(msg)

    def error(self, msg):
        print(msg)


def my_hook(d):
    if d['status'] == 'finished':
        print('Done downloading, now converting ...')


def get_my_ydl(directory=os.path.dirname(os.path.abspath(__file__))):
    ydl = None
    outtmpl = None
    if ut.check_directory(directory):
        outtmpl = os.path.join(directory, '%(title)s.%(ext)s')
        ydl_opts = {'format': 'bestaudio/best',
                    'postprocessors': [{'key': 'FFmpegExtractAudio',
                                        'preferredcodec': 'mp3',
                                        'preferredquality': '320'}],
                    'outtmpl': outtmpl,
                    'logger': MyLogger(),
                    'progress_hooks': [my_hook],
                    'verbose': False,
                    'ignoreerrors': False,
                    'external_downloader': 'ffmpeg',
                    'nocheckcertificate': True}
                    # 'external_downloader_args': "-j 8 -s 8 -x 8 -k 5M"}
                    # 'maxBuffer': 'Infinity'}
                    #  it uses multiple connections for speed up the downloading
                    #  'external-downloader': 'ffmpeg'}
        ydl = yt_dlp.YoutubeDL(ydl_opts)
        ydl.cache.remove()
        import time
        time.sleep(.5)
    return ydl

def clean_filename(name):
    """
    Remove emojis, special characters, and leading/trailing spaces from the filename.
    """
    # Remove all non-alphanumeric characters except spaces and hyphens
    cleaned_name = re.sub(r'[^a-zA-Z0-9\s\-\:]', '', name)
    # Replace multiple spaces with a single space
    cleaned_name = re.sub(r'\s+', ' ', cleaned_name).strip()
    return cleaned_name


def audio_from_url(url, name, path_output, errors=[]):
    """
    Download audio from a url.
        url : str
            url of the video (after watch?v= in youtube)
        name : str
            used to store the data
        path_output : str
            path for storing the data
    """
    error = None

    # ydl(youtube_dl.YoutubeDL): extractor
    # ydl = get_my_ydl(path_output)

    # ydl.params['outtmpl'] = os.path.join(
    # ydl.params['outtmpl'].replace('%(title)s', name)
    #                      .replace('%(ext)s', ydl.params['postprocessors'][0]['preferredcodec']))

#     ydl.params['outtmpl'] = ydl.params['outtmpl'] % {
#     'ext': ydl.params['postprocessors'][0]['preferredcodec'],
#     'title': name
# }

    # if ydl:
    #     print ("Downloading " + url)
    #     try:
    #         ydl.download([base_url + url])
    #     except Exception as e:
    #         print(e)
    #         error = e
    # if error:
    #     errors.append([name, url, error])
    # return
    try:
        # Clean the file name to remove unwanted symbols
        name = clean_filename(name)
        print(f"Downloading audio for: {name} ({url})")
        ydl = get_my_ydl(path_output)
        ydl.download([base_url + url])
    except Exception as e:
        print(f"Error downloading {name}: {e}")
        error = e
    if error:
        errors.append([name, url, error])
    return
