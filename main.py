"""
Author: Prateek Rashmi Wagh
https://www.udemy.com/course/100-days-of-code/learn/lecture/45090307#questions/22334943

Modified: John Patmore

"""

from tkinter import *
from pytubefix import YouTube
from pytubefix.exceptions import RegexMatchError
from pytubefix.cli import on_progress

SAVE_PATH = "./Downloaded_Content"
CHARCOAL_BLACK = "#36454F"
WARM_WHITE = "#F5F5F5"
ICE_BLUE = "#E0FFFF"
SMALL_FONT = "Roboto 15 bold"
MEDIUM_FONT = "Roboto 25 bold"
LARGE_FONT = "Roboto 35 bold"

scheduler = None


def on_change(*args):
    global scheduler
    # Cancel scheduler upon content change
    if scheduler:
        input_box.after_cancel(scheduler)
    # Create a new scheduler to execute the call one second later
    scheduler = input_box.after(1000, get_title)


def get_title():
    url = input_box.get()
    if url:
        try:
            yt = YouTube(url=url)
            title_label.config(text=yt.title)
            author_label.config(text=yt.author)
        except RegexMatchError:
            title_label.config(text="")
            author_label.config(text="")
            pass


def download_video():
    url = input_box.get()
    yt = YouTube(url, on_progress_callback=on_progress)

    # Get the streams with the highest resolution video and best quality audio
    video = yt.streams.filter(file_extension='mp4', only_video=True).get_highest_resolution(progressive=False)
    audio = yt.streams.filter(file_extension='mp4', only_audio=True).order_by("abr")[-1]

    # Download the streams
    video.download(output_path=SAVE_PATH)
    audio.download(output_path=SAVE_PATH)


"""
After downloading separate video and audio, combine using:
ffmpeg -i "video_filename.mp4" -i "audio_filename.m4a" -acodec copy -vcodec copy "out_filename.mp4"
"""


window = Tk()
window.title("YouTube Downloader")
window.config(padx=50, pady=50, bg=CHARCOAL_BLACK)

main_label = Label(text="YouTube Video Downloader", font=LARGE_FONT, fg=WARM_WHITE, bg=CHARCOAL_BLACK)
main_label.grid(column=1, row=0)

sub_title_label = Label(text="\U0001f3a5 \U0001f3ac \U0001f39f \U0001f3ab", font=LARGE_FONT, fg=ICE_BLUE, bg=CHARCOAL_BLACK)
sub_title_label.grid(column=1, row=1)

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

download_button = Button(text="Download", width=25, height=2, command=download_video, font=SMALL_FONT)
download_button.grid(column=1, row=6)

window.mainloop()
