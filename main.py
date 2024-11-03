"""
Author: Prateek Rashmi Wagh
https://www.udemy.com/course/100-days-of-code/learn/lecture/45090307#questions/22334943
"""

from tkinter import *
from pytubefix import YouTube

SAVE_PATH = "./Downloaded_Content"
CHARCOAL_BLACK = "#36454F"
WARM_WHITE = "#F%F%F%"
ICE_BLUE = "#E0FFFF"
SMALL = ("Roboto", 15, "bold")
STYLE = ("Roboto", 35, "bold")


def download_video():
    url = YouTube(link.get())
    video = url.streams.get_highest_resolution()
    video.download(output_path=SAVE_PATH)
    result_label = Label(text="Video downloaded successfully!", font=SMALL, fg=ICE_BLUE, bg=CHARCOAL_BLACK)
    result_label.grid(column=1, row=5)


window = Tk()
window.title("YouTube Downloader")
window.config(padx=50, pady=50, bg=CHARCOAL_BLACK)

title_label = Label(text="YouTube Video Downloader", font=STYLE, fg=WARM_WHITE, bg=CHARCOAL_BLACK)
title_label.grid(column=1, row=0)

sub_title_label = Label(text="icons", font=STYLE, fg=ICE_BLUE, bg=CHARCOAL_BLACK)
sub_title_label.grid(column=1, row=1)

inst_label = Label(text="Paste the YouTube link here:", font=SMALL, fg=WARM_WHITE, bg=CHARCOAL_BLACK)
inst_label.grid(column=1, row=2)

link = StringVar()

input_box = Entry(width=80, bg="white", borderwidth=5, relief="flat", textvariable=link, font=("Roberto, 10"))
input_box.grid(column=1, row=3, padx=25, pady=25)

download_button = Button(text="Download", width=25, height=2, command=download_video, font=SMALL)
download_button.grid(column=1, row=4)

window.mainloop()
