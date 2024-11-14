from pytubefix import YouTube, Stream
from pytubefix.cli import on_progress


url = "https://www.youtube.com/watch?v=oRTuBS9uFsA"
SAVE_PATH = "./Downloaded_Content"

yt = YouTube(url, on_progress_callback=on_progress)
# print(yt.title)

# print(yt.streams.filter(file_extension='mp4'))
"""
[
	<Stream: itag="18" mime_type="video/mp4" res="360p" fps="24fps" vcodec="avc1.42001E" acodec="mp4a.40.2" progressive="True" type="video">, 
	<Stream: itag="137" mime_type="video/mp4" res="1080p" fps="24fps" vcodec="avc1.640028" progressive="False" type="video">, 
	<Stream: itag="136" mime_type="video/mp4" res="720p" fps="24fps" vcodec="avc1.64001f" progressive="False" type="video">, 
	<Stream: itag="135" mime_type="video/mp4" res="480p" fps="24fps" vcodec="avc1.4d401e" progressive="False" type="video">, 
	<Stream: itag="134" mime_type="video/mp4" res="360p" fps="24fps" vcodec="avc1.4d401e" progressive="False" type="video">, 
	<Stream: itag="133" mime_type="video/mp4" res="240p" fps="24fps" vcodec="avc1.4d4015" progressive="False" type="video">, 
	<Stream: itag="160" mime_type="video/mp4" res="144p" fps="24fps" vcodec="avc1.4d400c" progressive="False" type="video">, 
	<Stream: itag="139" mime_type="audio/mp4" abr="48kbps" acodec="mp4a.40.5" progressive="False" type="audio">, 
	<Stream: itag="140" mime_type="audio/mp4" abr="128kbps" acodec="mp4a.40.2" progressive="False" type="audio">
]
"""
# Get the streams with the highest resolution video and best quality audio
video = yt.streams.filter(file_extension='mp4', only_video=True).get_highest_resolution(progressive=False)
audio = yt.streams.filter(file_extension='mp4', only_audio=True).order_by("abr")[-1]

# Download the streams
video.download(output_path=SAVE_PATH)
audio.download(output_path=SAVE_PATH)

