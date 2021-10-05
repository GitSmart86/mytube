import os
import re
import subprocess
import eyed3
import string
from eyed3.id3.frames import ImageFrame
import shutil
import urllib
from moviepy.editor import *
from pytube import YouTube
from pytube import Playlist
import mimetypes
from mutagen.mp4 import MP4, MP4Cover


#############
#
#   CONST
#
#############

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

STORAGE_PATH = BASE_DIR + "\\data"
AUDIO_STORAGE_PATH = STORAGE_PATH + "\\audio"
VIDEO_STORAGE_PATH = STORAGE_PATH + "\\video"
IMAGE_STORAGE_PATH = STORAGE_PATH + "\\image"
FILE_IMG_PATH = os.path.join(BASE_DIR, "cover.jpg")
# FILE_OUTPUT_PATH = 'C:\\Users\\jonat\\Downloads\\pytube'


###############
#
#   Utility
#
###############

def strip_letters(string):
    return re.sub(r'[a-zA-Z]', '', string)


def strip_symbols(input_string):

    arr = ['`', '!', '@', '#', '$', '%', '^', '&', '*', '?',
           '=', '+', "'", '"', ',', '.', '/', '<', '>', ';', ':']

    return "".join(u for u in input_string if u not in (arr))


def print_list(list):
    for i in list:
        print(i)


def downloading():
    print("downloading")


def downloaded():
    print("finished downloading")


def join(array):
    result = ""
    while (len(array) > 0):
        result = os.path.join(result, array.pop(0))
    return result


def get_url_image(url):

    v_id = url.replace('https://www.youtube.com/watch?v=', '')

    v_id = v_id.split('&')[0]

    has_image = False

    try:
        urllib.request.URLopener().retrieve("https://i.ytimg.com/vi/" +
                                            v_id + "/maxresdefault.jpg", "cover.jpg")
        has_image = True
    except:
        try:
            urllib.request.URLopener().retrieve("https://i.ytimg.com/vi/" +
                                                v_id + "/hqdefault.jpg", "cover.jpg")
            has_image = True
        except:
            print("\n\n\n\nHAS NO IMAGE\n\n\n\n")

    return has_image


#############
#
#   Audio
#
#############

def download_audio_list(url, prefQuality):
    p = Playlist(url)
    for i in range(0, len(p)):
        download_audio(p[i], prefQuality, {'index': i, 'title': p.title})


def download_audio(url, prefQuality, playlist=None):
    print('downloading', url, '...')
    v = get_audio(url, prefQuality)
    convert_store_audio(v, playlist)


def get_audio(url, prefQuality):
    yt = YouTube(url)

    filtered_list = yt.streams.filter(type='audio')

    sorted_list = sorted(filtered_list, key=lambda x: int(
        strip_letters(x.abr)), reverse=False)

    # for x in sorted_list:
    #     print(strip_letters(x.abr), x)

    v = 0

    if prefQuality == "max":
        v = sorted_list[-1]

    elif prefQuality == "min":
        v = sorted_list[0]

    # print(v, '\n\n')

    v.download()

    cleaned_v_name = strip_symbols(yt.title)
    v_name = cleaned_v_name + "." + v.mime_type.split("/")[1]
    v_path = os.path.join(BASE_DIR, v_name)

    return {'file': v, 'file_name': v_name, 'name': cleaned_v_name, 'path': v_path, 'url': url}


def convert_store_audio(audio, playlist):

    new_file_path = join([
        AUDIO_STORAGE_PATH,
        strip_symbols(audio['name']) + ".mp3"
    ])

    path = audio['path']

    if(not os.path.isdir(AUDIO_STORAGE_PATH)):
        os.mkdir(AUDIO_STORAGE_PATH)

    if(os.path.exists(new_file_path)):
        os.remove(new_file_path)

    ffmpeg_cmd = f'ffmpeg -i "{path}" -vn "{new_file_path}"'
    os_cmd = f'cmd /c "{ffmpeg_cmd}"'

    # print(audio['path'], '\n\n', new_file_path, '\n\n')

    subprocess.call(os_cmd)

    if(os.path.exists(audio['path'])):
        os.remove(audio['path'])

    # set cover art

    has_image = get_url_image(audio['url'])

    file_type = mimetypes.MimeTypes().guess_type(new_file_path)[0]
    # print(file_type)

    audiofile = eyed3.load(new_file_path)
    # print(audiofile)

    if(audiofile is None):
        raise Exception("audiofile is None ! ")

    if (audiofile.tag == None):
        audiofile.initTag()

    if(has_image):
        audiofile.tag.images.set(ImageFrame.FRONT_COVER, open(
            FILE_IMG_PATH, 'rb').read(), 'image/jpeg')

    audiofile.tag.title = audio['name']
    audiofile.tag.album = playlist['title'] if playlist is not None else ''
    audiofile.tag.artist = '。'
    audiofile.tag.album_artist = '。'
    audiofile.tag.track_num = playlist['index'] if playlist is not None else 0
    audiofile.tag.save(version=eyed3.id3.ID3_V2_3)

    if(os.path.exists(FILE_IMG_PATH)):

        new_FILE_IMG_PATH = os.path.join(
            BASE_DIR, audio['file_name'].split('.')[0] + '.jpg')
        image_storage_path = os.path.join(
            IMAGE_STORAGE_PATH, audio['file_name'].split('.')[0] + '.jpg')

        os.rename(FILE_IMG_PATH, new_FILE_IMG_PATH)

        if(os.path.exists(image_storage_path)):
            os.remove(image_storage_path)

        shutil.move(new_FILE_IMG_PATH, image_storage_path)


#############
#
#   Video
#
#############


def download_video_list(url, prefQuality):
    p = Playlist(url)
    for i in range(0, len(p)):
        download_video(p[i], prefQuality)


def download_video(url, prefQuality):
    print('downloading', url, '...')
    # get video 1st, else risk file overridding error !
    v = get_video(url, prefQuality)
    # print("got v ", v, "\n\n")
    a = get_audio(url, prefQuality)
    # print("got a ", a, "\n\n")
    merge_store_video(a, v)


def get_video(url, prefQuality):
    yt = YouTube(url)

    filtered_list = yt.streams.filter(
        type='video').filter(
        mime_type='video/mp4')

    sorted_list = sorted(filtered_list, key=lambda x: int(
        strip_letters(x.resolution)), reverse=False)

    # for x in sorted_list:
    # print(strip_letters(x.resolution), x)

    v = 0

    if prefQuality == "max":
        v = sorted_list[-1]

    elif prefQuality == "min":
        v = sorted_list[0]

    # print(v)

    v.download()

    cleaned_v_name = strip_symbols(yt.title)
    v_name = cleaned_v_name + "." + v.mime_type.split("/")[1]
    v_path = os.path.join(BASE_DIR, v_name)

    new_v_name = cleaned_v_name + "_video." + v.mime_type.split("/")[1]
    new_v_path = os.path.join(BASE_DIR, new_v_name)

    if(os.path.exists(new_v_path)):
        os.remove(new_v_path)

    os.rename(v_path, new_v_path)

    return {'file': v, 'file_name': new_v_name, 'name': cleaned_v_name, 'path': new_v_path, 'url': url}


def merge_store_video(audio, video):
    new_v_path = os.path.join(VIDEO_STORAGE_PATH, video['file_name'])

    if(not os.path.isdir(VIDEO_STORAGE_PATH)):
        os.mkdir(VIDEO_STORAGE_PATH)

    if(os.path.exists(new_v_path)):
        os.remove(new_v_path)

    # ffmpeg_cmd = 'ffmpeg -i "'+video['file_name']+'" -i "'+audio['file_name'] + \
    #     '" -c:v copy -c:a copy -map 0:v:0 -map 1:a:0 "'+new_v_path+'"'

    ffmpeg_cmd = 'ffmpeg -i "'+video['file_name']+'" -i "'+audio['file_name'] + \
        '" -c:v copy -c:a copy -map 0:v:0 -map 1:a "'+new_v_path+'"'

    os_cmd = f'cmd /c "{ffmpeg_cmd}"'

    subprocess.call(os_cmd)

    if(os.path.exists(video['path'])):
        os.remove(video['path'])

    if(os.path.exists(audio['path'])):
        os.remove(audio['path'])

    has_image = get_url_image(video['url'])

    if(has_image):
        videofile = MP4(new_v_path)
        videofile["\xa9nam"] = video['name']
        videofile["\xa9ART"] = "artist_"
        videofile["\xa9alb"] = "album_"

        with open("cover.jpg", "rb") as f:
            videofile["covr"] = [
                MP4Cover(f.read(), imageformat=MP4Cover.FORMAT_JPEG)
            ]

        videofile.save()

    if(os.path.exists(FILE_IMG_PATH)):
        os.remove(FILE_IMG_PATH)
