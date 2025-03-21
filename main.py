"""
Author: John Patmore (SadSack963)

Original concept: Prateek Rashmi Wagh
https://www.udemy.com/course/100-days-of-code/learn/lecture/45090307#questions/22334943
"""

from tkinter import *
from ffmpeg import FFmpeg  # pip install python-ffmpeg
from ffmpeg.errors import FFmpegError
from html import escape
from pytubefix import YouTube
from pytubefix.cli import on_progress
from pytubefix.exceptions import RegexMatchError, BotDetection
from urllib.error import HTTPError, URLError


import logging

from logger import start_logging
from settings import get_settings, check_ffmpeg

logger = logging.getLogger(__name__)

url_check_timer = None


def on_change(*args) -> None:
    global url_check_timer
    # Cancel scheduler upon content change
    if url_check_timer:
        input_box.after_cancel(url_check_timer)
    # Create a new scheduler to execute the call one second later
    url_check_timer = input_box.after(1000, get_title)


def get_title() -> None:
    def enable():
        title_label.config(text=yt.title)
        author_label.config(text=yt.author)
        output_box.delete(FIRST, LAST)  # Clear previous value
        output_box.insert(0, "OUTPUT_" + yt.title.replace(":", ""))  # Remove colons as they mess up ffmpeg
        download_button.config(state="normal")
        download_button.config(background=user_settings['colors']['greenButton'])

    def disable():
        title_label.config(text="")
        author_label.config(text="")
        output_box.delete(FIRST, LAST)
        download_button.config(state="disabled")
        download_button.config(background=user_settings['colors']['redButton'])

    url = get_user_input(input_box.get())
    if url:
        try:
            logging.info(f"Input URL: {url}")
            yt = YouTube(url=url, use_po_token=True)  # , client="WEB")  # , token_file="tokens.json")
            enable()
        except RegexMatchError as e:
            logging.error(f"URL RegexMatchError: [{e.args}] {e.pattern}")
            disable()
        except BotDetection as e:
            logging.error(f"URL BotDetection: {e.error_string}")
            disable()
    else:
        disable()


def get_user_input(data: str) -> str:
    # Sanitize user input
    return escape(data).strip()


def download_video() -> None:
    url = input_box.get()
    if url:
        filename = get_user_input(output_box.get()).rstrip(".mp4")
        try:
            yt = YouTube(url=url, on_progress_callback=on_progress, use_po_token=True)  # , client="WEB")  # , token_file="tokens.json")

            # Get the streams with the highest resolution video and best quality audio
            video_stream = yt.streams.filter(file_extension='mp4', only_video=True).get_highest_resolution(progressive=False)
            audio_stream = yt.streams.filter(file_extension='mp4', only_audio=True).order_by("abr")[-1]

            # Disable download_button and change text. Enable when finished or error
            download_button.config(state="disabled", text="Downloading")
            window.update()
            # TODO: Download options for video and audio

            # Download the streams
            logging.debug("Video download - start")
            video_path = video_stream.download(output_path=user_settings["savePath"])
            logging.debug("Video download - end")
            logging.debug("Audio download - start")
            audio_path = audio_stream.download(output_path=user_settings["savePath"])
            logging.debug("Audio download - end")
            merge(video_path, audio_path, filename)
        except RegexMatchError as e:
            logging.error(f'Video not found - {url}, RegexMatchError: {e.caller}, {e.pattern}')
            logging.debug("--- Check for updated pytubefix package ---")
            title_label.config(text="Video not found on YouTube.")  # TODO: Create function to change error colour, etc.
        except HTTPError as e:
            logging.error(f"HTTP error: [{e.code}] {e.reason}")
            title_label.config(text="HTTP Error.")
        except URLError as e:
            logging.error(f"URL error: {e.reason}")
            title_label.config(text="URL Error.")
        finally:
            download_button.config(state="normal", text="Download")


def merge(video_path: str, audio_path: str, filename: str) -> None:
    """
    After downloading separate video and audio, combine using:
    ffmpeg -i "video_filename.mp4" -i "audio_filename.m4a" -acodec copy -vcodec copy "out_filename.mp4"
    """
    destination_path = f'{user_settings["savePath"]}/{filename}.mp4'
    try:
        # Transcoding is slow. Keep the original codecs.
        ffmpeg = (
            FFmpeg(executable=user_settings["ffmpegPath"])
            .option("y")  # overwrite output files without asking
            .input(video_path)
            .input(audio_path)
            .output(destination_path, vcodec="copy", acodec="copy")
            )
        logging.debug("Merge - start")
        ffmpeg.execute()
        logging.debug("Merge - end")
    except FFmpegError as e:
        logging.error(f"FFmpeg error: [{e.arguments}] {e.message}")
        title_label.config(text=f"FFmpeg error: [{e.arguments}] {e.message}")
    else:
        logging.info(f"Success! Video and Audio merged - {destination_path}")
        title_label.config(text=f"Success! Saved to {destination_path}")


start_logging()
user_settings = get_settings()
check_ffmpeg(user_settings["ffmpegPath"])

# TODO: Add a screen for settings
# TODO: Add Entry box for FFmpeg path

window = Tk()
window.title("YouTube Downloader")
window.config(
    padx=50,
    pady=50,
    bg=user_settings['colors']['border'],
)

main_label = Label(
    text="YouTube Video Downloader",
    font=f"{user_settings['font']} {user_settings['fontSizes']['huge']} bold",
    fg=user_settings['colors']['titleText'],
    bg=user_settings['colors']['border']
)
main_label.grid(column=1, row=0, columnspan=2)

icons_label = Label(
    text="\U0001f3a5 \U0001f3ac \U0001f39f \U0001f3ab",
    font=f"{user_settings['font']} {user_settings['fontSizes']['huge']} bold",
    fg=user_settings['colors']['titleText'],
    bg=user_settings['colors']['border']
)
icons_label.grid(column=1, row=1, columnspan=2)

inst_label = Label(
    text="Paste the YouTube link here:",
    font=f"{user_settings['font']} {user_settings['fontSizes']['large']}",
    fg=user_settings['colors']['defaultText'],
    bg=user_settings['colors']['border']
)
inst_label.grid(column=1, row=2, columnspan=2)

link = StringVar()
link.trace_add('write', on_change)
input_box = Entry(
    width=80,
    bg=user_settings['colors']['background'],
    fg=user_settings['colors']['url'],
    borderwidth=5,
    relief="sunken",
    textvariable=link,
    font=f"{user_settings['font']} {user_settings['fontSizes']['normal']}",
)
input_box.grid(column=1, row=3, columnspan=2)

title_label = Label(
    text="",
    font=f"{user_settings['font']} {user_settings['fontSizes']['normal']}",
    fg=user_settings['colors']['defaultText'],
    bg=user_settings['colors']['border']
)
title_label.grid(column=1, row=4, pady=5, columnspan=2)

author_label = Label(
    text="",
    font=f"{user_settings['font']} {user_settings['fontSizes']['normal']}",
    fg=user_settings['colors']['defaultText'],
    bg=user_settings['colors']['border']
)
author_label.grid(column=1, row=5, pady=5, columnspan=2)

# TODO: Add check boxes for video and audio choices

output_label = Label(
    text="Output Filename",
    font=f"{user_settings['font']} {user_settings['fontSizes']['large']}",
    fg=user_settings['colors']['defaultText'],
    bg=user_settings['colors']['border']
)
output_label.grid(column=1, row=6)

output_box = Entry(
    width=80,
    bg=user_settings['colors']['background'],
    fg=user_settings['colors']['defaultText'],
    borderwidth=5,
    relief="sunken",
    font=f"{user_settings['font']} {user_settings['fontSizes']['normal']}",
)
output_box.grid(column=2, row=6)

download_button = Button(
    text="Download",
    width=12,
    height=1,
    command=download_video,
    font=f"{user_settings['font']} {user_settings['fontSizes']['huge']}",
    background=user_settings['colors']['redButton'],
    default="disabled",
)
download_button.grid(column=1, row=7, columnspan=2)

# TODO: Add check boxes to delete source files.
# TODO: Add a progress bar!

window.mainloop()
