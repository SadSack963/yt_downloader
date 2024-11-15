"""
Author: Prateek Rashmi Wagh
https://www.udemy.com/course/100-days-of-code/learn/lecture/45090307#questions/22334943

Modified: John Patmore

"""

from tkinter import *
from urllib.error import HTTPError, URLError
from pytubefix import YouTube
from pytubefix.exceptions import RegexMatchError
from pytubefix.cli import on_progress
from ffmpeg import FFmpeg  # pip install python-ffmpeg
from ffmpeg.errors import FFmpegError
import html


# TODO: Create a configuration file for user settings
SAVE_PATH = "./Downloaded_Content"
FFMPEG_PATH = r"C:\Program Files\FFmpeg For Audacity\ffmpeg-7.0.2-full_build-shared\bin\ffmpeg.exe"  # Default "ffmpeg"

CHARCOAL_BLACK = "#36454F"
WARM_WHITE = "#F5F5F5"
ICE_BLUE = "#E0FFFF"
SMALL_FONT = "Roboto 15 bold"
MEDIUM_FONT = "Roboto 25 bold"
LARGE_FONT = "Roboto 35 bold"

scheduler = None

# TODO: Check for FFmpeg on user's system - issue notification if not found


def on_change(*args) -> None:
    global scheduler
    # Cancel scheduler upon content change
    if scheduler:
        input_box.after_cancel(scheduler)
    # Create a new scheduler to execute the call one second later
    scheduler = input_box.after(1000, get_title)


def get_title() -> None:
    url = get_user_input(input_box.get())
    if url:
        try:
            yt = YouTube(url=url)
            title_label.config(text=yt.title)
            author_label.config(text=yt.author)
            # TODO: Enable download button
        except RegexMatchError:
            title_label.config(text="")  # TODO: Pull these out into a function
            author_label.config(text="")
    else:
        title_label.config(text="")
        author_label.config(text="")


def get_user_input(data: str) -> str:
    # Sanitize user input
    return html.escape(data).strip()


def download_video() -> None:
    url = input_box.get()
    if url:
        filename = get_user_input(output_box.get()).rstrip(".mp4")
        try:
            yt = YouTube(url, on_progress_callback=on_progress)

            # Get the streams with the highest resolution video and best quality audio
            video_stream = yt.streams.filter(file_extension='mp4', only_video=True).get_highest_resolution(progressive=False)
            audio_stream = yt.streams.filter(file_extension='mp4', only_audio=True).order_by("abr")[-1]

            # TODO: Disable download_button and change text. Enable when finished or error
            # TODO: Get the output filename

            # Download the streams
            video_path = video_stream.download(output_path=SAVE_PATH)
            audio_path = audio_stream.download(output_path=SAVE_PATH)
            merge(video_path, audio_path, filename)  # TODO: Create a field to enter the output filename
        except RegexMatchError:
            title_label.config(text="Video not found on YouTube.")  # TODO: Create function to change error colour, etc.
        except HTTPError as e:
            print(f"HTTP error: [{e.code}] {e.reason}")
        except URLError as e:
            print(f"URL error: {e.reason}")


def merge(video_path: str, audio_path: str, filename: str) -> None:
    """
    After downloading separate video and audio, combine using:
    ffmpeg -i "video_filename.mp4" -i "audio_filename.m4a" -acodec copy -vcodec copy "out_filename.mp4"
    """
    destination_path = f"{SAVE_PATH}/{filename}.mp4"
    try:
        ffmpeg = (
            FFmpeg(executable=FFMPEG_PATH)
            .option("y")  # overwrite output files without asking
            .input(video_path)
            .input(audio_path)
            .output(destination_path, vcodec="copy", acodec="copy")
            )
        ffmpeg.execute()
    except FFmpegError as e:
        title_label.config(text=f"FFmpeg error: [{e.arguments}] {e.message}")
    else:
        title_label.config(text="Success!")  # TODO: Something a bit more informative please :)


window = Tk()
window.title("YouTube Downloader")
window.config(padx=50, pady=50, bg=CHARCOAL_BLACK)

main_label = Label(text="YouTube Video Downloader", font=LARGE_FONT, fg=WARM_WHITE, bg=CHARCOAL_BLACK)
main_label.grid(column=1, row=0)

icons_label = Label(text="\U0001f3a5 \U0001f3ac \U0001f39f \U0001f3ab", font=LARGE_FONT, fg=ICE_BLUE, bg=CHARCOAL_BLACK)
icons_label.grid(column=1, row=1)

inst_label = Label(text="Paste the YouTube link here:", font=SMALL_FONT, fg=WARM_WHITE, bg=CHARCOAL_BLACK)
inst_label.grid(column=1, row=2)

link = StringVar()
link.trace_add('write', on_change)
input_box = Entry(width=80, bg="white", borderwidth=5, relief="flat", textvariable=link, font="Roberto 10")
input_box.grid(column=1, row=3)

title_label = Label(text="", font=SMALL_FONT, fg=WARM_WHITE, bg=CHARCOAL_BLACK)
title_label.grid(column=1, row=4, pady=5)

author_label = Label(text="", font=SMALL_FONT, fg=WARM_WHITE, bg=CHARCOAL_BLACK)
author_label.grid(column=1, row=5, pady=5)

output_label = Label(text="Output Filename", font=SMALL_FONT, fg=WARM_WHITE, bg=CHARCOAL_BLACK)
output_label.grid(column=1, row=6)

output_box = Entry(width=80, bg="white", borderwidth=5, relief="flat", textvariable=link, font="Roberto 10")
output_box.grid(column=2, row=6)

download_button = Button(text="Download", width=25, height=2, command=download_video, font=SMALL_FONT)
download_button.grid(column=1, row=7)

window.mainloop()
