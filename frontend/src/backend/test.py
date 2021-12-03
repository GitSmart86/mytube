import mipitube
import sys

print("Hello world, ", str(sys.argv), '\nfirst param: ', str(sys.argv[0]))


def raise_error_url():
    raise ValueError("input url from 'argv[0]' was invalid.")


def validate_mode(mode):
    if mode != "audio" and mode != "video":
        raise ValueError(
            "input mode from 'argv[1]' was invalid. [Options: 'audio', 'video' ]")


def validate_quality(quality):
    if quality != "max" and quality != "min":
        raise ValueError(
            "input quality from 'argv[2]' was invalid. [Options: 'max', 'min' ]")


url = sys.argv[1]
mode = sys.argv[2]
quality = sys.argv[3]

validate_mode(mode)
validate_quality(quality)


if url.startswith("https://www.youtube.com/playlist?list="):

    if mode == "audio":
        mipitube.download_audio_list(url, quality)

    elif mode == "video":
        mipitube.download_video_list(url, quality)

elif url.startswith("https://www.youtube.com/watch?v="):

    if mode == "audio":
        mipitube.download_audio(url, quality)

    elif mode == "video":
        mipitube.download_video(url, quality)

else:
    raise_error_url()

# personal_playlist = 'https://www.youtube.com/playlist?list=PLQ7r1UnuOsj6beuqlYJjmOCPA7KRkCIA9'
# mipitube.download_video_list(personal_playlist, 'max')

# url = 'https://www.youtube.com/watch?v=9-sFa7peyGQ'
# mipitube.download_audio(url, 'max')

print('\n\nFinished!')
