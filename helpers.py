import os
import json
import re
from PIL import Image
from datetime import datetime

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

def calculate_time_difference(start_time_str, end_time_str):
    time_format = "%H:%M:%S"
    start_time_obj = datetime.strptime(start_time_str, time_format)
    end_time_obj = datetime.strptime(end_time_str, time_format)
    time_difference = end_time_obj - start_time_obj
    time_difference_str = str(time_difference)
    if time_difference.days < 0:
        time_difference_str = "-" + time_difference_str[1:]
    time_difference_str = time_difference_str[-8:]
    return time_difference_str


def is_valid_time(start_time_str, end_time_str):
    try:
        time_format = "%H:%M:%S"
        start_time_obj = datetime.strptime(start_time_str, time_format)
        end_time_obj = datetime.strptime(end_time_str, time_format)
    except:
        return False, "Start or end time not in valid format: hh:mm:ss"
    if start_time_obj >= end_time_obj:
        return False, "Start time cannot be greater than or equal to end time"
    return True, ""
