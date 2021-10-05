import mipitube

# personal_playlist = 'https://www.youtube.com/playlist?list=PLQ7r1UnuOsj4eKbL6cvbuWp66JCF4ChPP'
# mipitube.download_audio_list(personal_playlist, 'max')

url = 'https://www.youtube.com/watch?v=jQf5jL3a4iU&list=PLQ7r1UnuOsj5D0WaN9dq_FQpioYWpf4Te&index=1'
mipitube.download_audio(url, 'max')


print('\n\nFinished!')
