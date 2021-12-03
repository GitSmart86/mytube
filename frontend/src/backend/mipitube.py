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

FILE_PATH_COVER_ART = BASE_DIR + "\\cover.jpg"
STORAGE_PATH = BASE_DIR + "\\data"
STORAGE_PATH_AUDIO = STORAGE_PATH + "\\audio"
STORAGE_PATH_VIDEO = STORAGE_PATH + "\\video"
STORAGE_PATH_IMAGE = STORAGE_PATH + "\\image"


###############
#
#   Utility
#
###############


def dir_make(dir):
    if(not os.path.isdir(dir)):
        os.mkdir(dir)


def file_exists(path):
    return os.path.exists(path)


def file_delete(path):
    if(os.path.exists(path)):
        os.remove(path)


def file_rename(old_path, new_path):
    file_delete(new_path)
    os.rename(old_path, new_path)


def file_move(old_path, new_path):
    file_delete(new_path)
    shutil.move(old_path, new_path)


def strip_letters(string):
    return re.sub(r'[a-zA-Z]', '', string)


def strip_symbols(input_string):

    arr = ['`', '@', '#', '$', '%', '^', '&', '*', '?',
           '=', '+', "'", '"', ',', '.', '/', '<', '>', ';', ':', '|']

    return "".join(u for u in input_string if u not in (arr))


def print_list(list):
    for i in list:
        print(i)


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


def store_cover_art(old_path, new_name, playlist=None):

    if(file_exists(old_path)):

        new_name_path = BASE_DIR + '\\' + new_name

        file_rename(old_path, new_name_path)

        image_storage_dir = STORAGE_PATH_IMAGE
        if playlist is not None:
            image_storage_dir = os.path.join(
                image_storage_dir, playlist['title'])

        dir_make(image_storage_dir)
        image_storage_path = os.path.join(
            image_storage_dir, new_name)

        file_move(new_name_path, image_storage_path)


#############
#
#   Audio
#
#############


def download_audio_list(url, prefQuality):
    p = Playlist(url)
    for i in range(0, len(p)):
        print(f"\n\n[ {i+1} / {len(p)} ]    downloading {url}...\n\n")
        download_audio(p[i], prefQuality, {'index': i, 'title': p.title})


def download_audio(url, prefQuality, playlist=None):
    if playlist is None:
        print(f"\n\ndownloading {url}...\n\n")
    audio = get_audio(url, prefQuality)
    convert_store_audio(audio, playlist)


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

    audio_storage_path = ""
    if playlist is None:
        audio_storage_path = STORAGE_PATH_AUDIO
    else:
        audio_storage_path = STORAGE_PATH_AUDIO + '\\' + playlist['title']

    new_file_path = join([
        audio_storage_path,
        strip_symbols(audio['name']) + ".mp3"
    ])

    path = audio['path']

    # convert file to mp3

    if(not os.path.isdir(STORAGE_PATH_AUDIO)):
        os.mkdir(STORAGE_PATH_AUDIO)

    if(not os.path.isdir(audio_storage_path)):
        os.mkdir(audio_storage_path)

    file_delete(new_file_path)

    ffmpeg_cmd = f'ffmpeg -i "{path}" -vn "{new_file_path}"'
    os_cmd = f'cmd /c "{ffmpeg_cmd}"'

    subprocess.call(os_cmd)

    file_delete(audio['path'])

    # set cover art

    has_image = get_url_image(audio['url'])

    audiofile = eyed3.load(new_file_path)

    if(audiofile is None):
        raise Exception("audiofile is None ! ")

    if (audiofile.tag == None):
        audiofile.initTag()

    if(has_image):
        audiofile.tag.images.set(ImageFrame.FRONT_COVER, open(
            FILE_PATH_COVER_ART, 'rb').read(), 'image/jpeg')

    audiofile.tag.title = audio['name']
    audiofile.tag.album = playlist['title'] if playlist is not None else ''
    audiofile.tag.artist = '。'
    audiofile.tag.album_artist = '。'
    audiofile.tag.track_num = playlist['index'] if playlist is not None else 0
    audiofile.tag.save(version=eyed3.id3.ID3_V2_3)

    # save copy of img

    new_name = audio['file_name'].split('.')[0] + '.jpg'

    store_cover_art(
        FILE_PATH_COVER_ART,
        new_name,
        playlist
    )


#############
#
#   Video
#
#############


def download_video_list(url, prefQuality):
    p = Playlist(url)
    for i in range(0, len(p)):
        print(f"\n\n[ {i+1} / {len(p)} ]    downloading {url}...\n\n")
        download_video(p[i], prefQuality, {'index': i, 'title': p.title})


def download_video(url, prefQuality, playlist=None):
    if playlist is None:
        print(f"\n\ndownloading {url}...\n\n")

    v = get_video(url, prefQuality)
    a = get_audio(url, prefQuality)
    merge_store_video(a, v, playlist)


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

    file_rename(v_path, new_v_path)

    return {'file': v, 'file_name': new_v_name, 'name': cleaned_v_name, 'path': new_v_path, 'url': url}


def merge_store_video(audio, video, playlist=None):

    # merge audio + video

    new_v_dir = STORAGE_PATH_VIDEO

    if playlist is not None:
        new_v_dir = os.path.join(new_v_dir, playlist['title'])

    new_v_path = os.path.join(new_v_dir, video['file_name'])

    dir_make(new_v_dir)
    file_delete(new_v_path)

    # ffmpeg_cmd = 'ffmpeg -i "'+video['file_name']+'" -i "'+audio['file_name'] + \
    #     '" -c:v copy -c:a copy -map 0:v:0 -map 1:a:0 "'+new_v_path+'"'

    ffmpeg_cmd = 'ffmpeg -i "'+video['file_name']+'" -i "'+audio['file_name'] + \
        '" -c:v copy -c:a copy -map 0:v:0 -map 1:a "'+new_v_path+'"'

    os_cmd = f'cmd /c "{ffmpeg_cmd}"'

    subprocess.call(os_cmd)

    file_delete(video['path'])
    file_delete(audio['path'])

    # set new file attributes

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

    # save copy of img

    new_name = video['file_name'].split('.')[0] + '.jpg'

    store_cover_art(
        FILE_PATH_COVER_ART,
        new_name,
        playlist
    )
