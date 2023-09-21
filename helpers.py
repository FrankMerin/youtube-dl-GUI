import os
import json
import subprocess
import re
import threading
from PIL import Image, ImageTk
import random

config_file = "config.json"  # Set the path to your config file

def load_config():
    if not os.path.exists(config_file) or os.path.getsize(config_file) == 0:
        with open(config_file, "w") as f:
            json.dump({}, f)
    with open(config_file, "r") as f:
        config = json.load(f)
    default_config = {
        "ffmpeg_path": "",
        "output_directory": ""
    }
    default_config.update(config)
    return default_config

def count_png_files(folder_path):
    png_count = 0
    if not os.path.exists(folder_path) or not os.path.isdir(folder_path):
        return png_count  
    for filename in os.listdir(folder_path):
        if filename.endswith(".png"):
            png_count += 1
    return png_count

def extract_frames_from_gif(input_gif_path, output_folder):
    os.makedirs(output_folder, exist_ok=True)
    with Image.open(input_gif_path) as img:
        try:
            frame_number = 1
            while True:
                img.save(os.path.join(output_folder, f"frame{frame_number}.png"))
                frame_number += 1
                img.seek(img.tell() + 1)
        except EOFError:
            pass
    return frame_number - 1

def clean_youtube_url(url):
    clean_url = re.sub(r'(&list=|&t=).*', '', url)
    return clean_url