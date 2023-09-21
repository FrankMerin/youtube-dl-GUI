import tkinter as tk
from tkinter import ttk
import subprocess
import re
import threading
from PIL import Image, ImageTk
import os
import random
import json
import yt_dlp
from threading import Thread

from helpers import (
    load_config,
    count_png_files,
    extract_frames_from_gif,
    clean_youtube_url,
)


file_types = ["M4A", "MP3", 'MP4']
CONFIG_FILE = "config.json"
IMAGE_FOLDER = 'frames'

configs = load_config()
ffmpeg_path = configs["ffmpeg_path"]
output_directory = configs["output_directory"]

continue_animation = True
random_delay = random.randint(10, 130)

def set_custom_paths():
    global ffmpeg_path, output_directory
    custom_ffmpeg_path = ffmpeg_path_entry.get()
    custom_output_directory = output_directory_entry.get()

    if custom_ffmpeg_path:
        ffmpeg_path = custom_ffmpeg_path

    if custom_output_directory:
        if not custom_output_directory.endswith('\\'):
            custom_output_directory = custom_output_directory + '\\'
        output_directory = custom_output_directory

    config = {
        "ffmpeg_path": ffmpeg_path,
        "output_directory": output_directory
    }
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f)

def download_content():
    try:
        global output_directory, continue_animation
        download_button.config(state=tk.DISABLED)
        status_label.config(text="")
        continue_animation = True
        animate_spinner()

        youtube_url = url_entry.get()

        if not os.path.exists(output_directory):
            os.makedirs(output_directory)
        
        if not os.path.isfile(ffmpeg_path):
            raise FileNotFoundError("ffmpeg_path not found in the specified path")

        if not re.search(r'(youtube\.com|youtu\.be)', youtube_url):
            raise ValueError("Invalid YouTube URL")

        clean_url = clean_youtube_url(youtube_url)
        file_type = selected_file_type.get()

        ydl_opts = {
            'format': f'bestaudio/best' if file_type in ('M4A', 'MP3') else f'bestvideo[ext={file_type.lower()}]+bestaudio[ext={file_type.lower()}]/best[ext={file_type.lower()}]/best',
            'outtmpl': os.path.join(output_directory, '%(title)s.%(ext)s'),
            'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': file_type.lower(), 'preferredquality': '0'}] if file_type in ('M4A', 'MP3') else [],
            'ffmpeg_location': 'C:\\Users\\godsw\\OneDrive\\Documents\\applet\\build\\ffmpeg.exe'
        }

        def run_download():
            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([clean_url])
                root.after(0, lambda: update_status("Download Complete!"))
            except yt_dlp.DownloadError as e:
                root.after(0, lambda: update_status(f"Error: {e}"))

        Thread(target=run_download).start()

    except FileNotFoundError as e:
        root.after(0, lambda: update_status(f"Error: {e}"))
    except ValueError as e:
        root.after(0, lambda: update_status(f"Error: {e}"))


def update_status(message):
    global continue_animation
    download_button.config(state=tk.NORMAL)
    status_label.config(text=message)
    spinner_label.grid_forget()
    continue_animation = False

def animate_spinner():
    global spinner_label
    spinner_label = ttk.Label(root)
    spinner_label.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

    global spinner_index
    spinner_index = 1
    animate()

def animate():
    global spinner_index, png_count, random_delay
    frame_path = os.path.join(IMAGE_FOLDER, f'frame{spinner_index}.png')
    image = Image.open(frame_path)
    spinner_image = ImageTk.PhotoImage(image)

    spinner_label.config(image=spinner_image)
    spinner_label.image = spinner_image

    spinner_index = (spinner_index % png_count) + 1
    if spinner_index == 2:
        random_delay = random.randint(5, 100)
    if continue_animation:
        root.after(random_delay, animate)

png_count = count_png_files(IMAGE_FOLDER)
if png_count == 0:
    png_count = extract_frames_from_gif("loading.gif", IMAGE_FOLDER)

root = tk.Tk()
root.title("YouTube Downloader")

selected_file_type = tk.StringVar(root)

file_type_label = ttk.Label(root, text="Select File Type:")
file_type_combobox = ttk.Combobox(root, textvariable=selected_file_type, values=file_types, width=6)
file_type_combobox.set(file_types[0])


url_label = ttk.Label(root, text="YouTube Video or Playlist URL:")
url_entry = ttk.Entry(root, width=40)
download_button = ttk.Button(root, text="Download", command=download_content)
status_label = ttk.Label(root, text="")

ffmpeg_path_label = ttk.Label(root, text="Current ffmpeg Path:")
ffmpeg_path_entry = ttk.Entry(root, width=40)
output_directory_label = ttk.Label(root, text="Current Output Directory:")
output_directory_entry = ttk.Entry(root, width=40)
set_paths_button = ttk.Button(root, text="Set Paths", command=set_custom_paths)

url_label.grid(row=0, column=0, padx=10, pady=10)
url_entry.grid(row=0, column=1, padx=10, pady=10)
file_type_label.grid(row=1, column=0, padx=10, pady=10, sticky="w") 
file_type_combobox.grid(row=1, column=1, padx=10, pady=10, sticky="w")  
download_button.grid(row=1, column=1, padx=100, pady=10, sticky="w")
status_label.grid(row=2, column=0, columnspan=2, padx=10, pady=5)

ffmpeg_path_label.grid(row=4, column=0, padx=10, pady=10)
ffmpeg_path_entry.grid(row=4, column=1, padx=10, pady=10)
output_directory_label.grid(row=5, column=0, padx=10, pady=10)
output_directory_entry.grid(row=5, column=1, padx=10, pady=10)
set_paths_button.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

ffmpeg_path_entry.insert(0, ffmpeg_path)
output_directory_entry.insert(0, output_directory)

root.mainloop()