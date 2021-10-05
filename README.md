1. Installation / Setup :

If 'virtual environment' is not already installed:
<code>pip install virtual env</code>

Else continue:
<code>cd mytube</code>
<code>virtualenv venv</code>
<code>env</code>
<code>pip install -r requirements.txt</code>

2. Obtain a YouTube video or playlist url of your choice, and then edit 'backend/test.py' according to the format list below.

3. run the test file by optionally entering the command <code>test</code>.

<br/><br/>

Test.py Configuration :
ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ

<code><preferred_download_quality></code> = 'max' | 'min'
<code><\*url></code> = 'https://www.youtube.com/...'

<br/>

Download Single Video's Audio :
<code>mipitube.download_audio(<video_url>, <preferred_download_quality>)</code>

<br/>

Download Single Playlist's Audio :
<code>mipitube.download_audio_list(<playlist_url>, <preferred_download_quality>)</code>

<br/>

Download Single Video's Video :
<code>mipitube.download_video(<video_url>, <preferred_download_quality>)</code>

<br/>

Download Single Playlist's Video :
<code>mipitube.download_video_list(<playlist_url>, <preferred_download_quality>)</code>
