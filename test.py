import mipitube

keepers = 'https://www.youtube.com/playlist?list=PLQ7r1UnuOsj4eKbL6cvbuWp66JCF4ChPP'
# mipitube.download_audio_list(keepers, 'max')


url = 'https://www.youtube.com/playlist?list=PLQ7r1UnuOsj4eKbL6cvbuWp66JCF4ChPP'

# url = 'https://www.youtube.com/watch?v=CSI6cie_Ci8&list=PL0F37A4B366BB6AA2&index=1'

# url = 'https://www.youtube.com/watch?v=6Y4PEqvk0Jg&list=PLQ7r1UnuOsj5D0WaN9dq_FQpioYWpf4Te&index=2'
mipitube.download_audio_list(url, 'max')
# mipitube.download_video(url, 'max')
