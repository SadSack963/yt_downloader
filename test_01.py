from pytubefix import YouTube
from pytubefix.cli import on_progress

url = "https://youtu.be/4OBJhKvLJ0c?si=Y2j2l9rzV1uPCMix"
SAVE_PATH = "./Downloaded_Content"

yt = YouTube(url, on_progress_callback=on_progress)
# print(yt.title)
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
print(yt.streams.filter(file_extension='mp4'))

# 1080p video
stream = yt.streams.get_by_itag(137)
stream.download(output_path=SAVE_PATH)
# 128kbps audio
# stream = yt.streams.get_by_itag(140)
# stream.download(output_path=SAVE_PATH)

exit()

ys = yt.streams.get_highest_resolution()
ys.download()
