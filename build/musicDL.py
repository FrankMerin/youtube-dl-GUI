import tkinter as tk
from tkinter import ttk
import subprocess
import re
import threading
from PIL import Image, ImageTk
import os
import random
import json
import sys

from helpersDL import (
    load_config,
    count_png_files,
    extract_frames_from_gif,
    clean_youtube_url,
)


base_path = getattr(sys, '_MEIPASS', os.getcwd())

IMAGE_FOLDER = 'frames'


youtube_dl_path = os.path.join(base_path, "yt-dlp.exe")

config_directory = os.path.join(os.path.expanduser("~"), ".musicDL")
if not os.path.exists(config_directory):
    os.makedirs(config_directory)
CONFIG_FILE = os.path.join(config_directory, "config.json")

configs = load_config()
output_directory = configs["output_directory"]
continue_animation = True
random_delay = random.randint(10, 130)

def set_custom_paths():
    global output_directory

    custom_output_directory = output_directory_entry.get()

    if custom_output_directory:
        if not custom_output_directory.endswith('\\'):
            custom_output_directory = custom_output_directory + '\\'
        output_directory = custom_output_directory
    config = {
        "output_directory": output_directory
    }
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f)

def download_mp3():
    try:
        global output_directory, continue_animation
        download_button.config(state=tk.DISABLED)
        status_label.config(text="")
        continue_animation = True
        animate_spinner()


        youtube_url = url_entry.get()

        if not os.path.exists(output_directory):
            os.makedirs(output_directory)

        if not re.search(r'(youtube\.com|youtu\.be)', youtube_url):
            raise ValueError("Invalid YouTube URL")
        
        clean_url = clean_youtube_url(youtube_url)
        youtube_dl_command = f'{youtube_dl_path} -o "{output_directory}%(title)s.%(ext)s" -f bestaudio --extract-audio --audio-format mp3 --audio-quality 0 {clean_url}'

        def run_download():
            try:
                subprocess.run(youtube_dl_command, shell=True, check=True)
                root.after(0, lambda: update_status("Download Complete!"))
            except subprocess.CalledProcessError as e:
                root.after(0, lambda: update_status(f"Error: {e}"))

        global download_thread
        download_thread = threading.Thread(target=run_download)
        download_thread.start()
    except Exception as e:
        update_status(f"Error: {e}")

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
    png_count = extract_frames_from_gif(os.path.join(base_path, "loading.gif"), IMAGE_FOLDER)


root = tk.Tk()
root.title("YouTube MP3 Downloader")

url_label = ttk.Label(root, text="YouTube Video or Playlist URL:")
url_entry = ttk.Entry(root, width=40)
download_button = ttk.Button(root, text="Download MP3", command=download_mp3)
status_label = ttk.Label(root, text="")

output_directory_label = ttk.Label(root, text="Current Output Directory:")
output_directory_entry = ttk.Entry(root, width=40)
set_paths_button = ttk.Button(root, text="Set Paths", command=set_custom_paths)

url_label.grid(row=0, column=0, padx=10, pady=10)
url_entry.grid(row=0, column=1, padx=10, pady=10)
download_button.grid(row=1, column=0, columnspan=2, padx=10, pady=0)
status_label.grid(row=2, column=0, columnspan=2, padx=10, pady=5)


output_directory_label.grid(row=5, column=0, padx=10, pady=10)
output_directory_entry.grid(row=5, column=1, padx=10, pady=10)
set_paths_button.grid(row=6, column=0, columnspan=2, padx=10, pady=10)


output_directory_entry.insert(0, output_directory)

root.mainloop()
