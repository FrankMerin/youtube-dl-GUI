import tkinter as tk
from tkinter import ttk
import subprocess
import re
import threading
from PIL import Image, ImageTk
import os

default_youtube_dl_path = r'C:\Users\......\youtube-dl.exe'  # Default youtube-dl.exe path
default_output_directory = 'C:\\Users\\The_Best_Music\\'  # Default output path
youtube_dl_path = default_youtube_dl_path
output_directory = default_output_directory
image_folder = 'spinner_frames' 


def set_custom_paths():
    global youtube_dl_path, output_directory
    custom_youtube_dl_path = youtube_dl_path_entry.get()
    custom_output_directory = output_directory_entry.get()
    
    if custom_youtube_dl_path:
        youtube_dl_path = custom_youtube_dl_path
    
    if custom_output_directory:
        output_directory = custom_output_directory

def clean_youtube_url(url):
    clean_url = re.sub(r'&list=.*', '', url)
    return clean_url


def download_mp3():
    try:
        global output_directory
        download_button.config(state=tk.DISABLED)
        status_label.config(text="")
        animate_spinner()

        if not os.path.isfile(youtube_dl_path):
            raise FileNotFoundError("youtube-dl not found in the specified path")

        youtube_url = url_entry.get()
        

        if not os.path.exists(output_directory):
            os.makedirs(output_directory)

        if not output_directory.endswith('\\'):
            output_directory = output_directory + '\\'

        if not re.search(r'youtube\.com', youtube_url):
            raise ValueError("Invalid YouTube URL")

        clean_url = clean_youtube_url(youtube_url)
        youtube_dl_command = f'{youtube_dl_path} -o "{output_directory}%(title)s.%(ext)s" -f bestaudio --extract-audio --audio-format mp3 --audio-quality 0 {clean_url}'

        def run_download():
            try:
                subprocess.run(youtube_dl_command, shell=True, check=True)
                app.after(0, lambda: update_status("Download Complete!"))
            except subprocess.CalledProcessError as e:
                app.after(0, lambda: update_status(f"Error: {e}"))
        
        global download_thread
        download_thread = threading.Thread(target=run_download)
        download_thread.start()
    except Exception as e:
        update_status(f"Error: {e}")
        
def update_status(message):
    download_button.config(state=tk.NORMAL)
    status_label.config(text=message)
    spinner_label.grid_forget()

def animate_spinner():
    global spinner_label
    spinner_label = ttk.Label(app)
    spinner_label.grid(row=3, column=0, columnspan=2, padx=10, pady=10)
    
    global spinner_index
    spinner_index = 1
    animate()

def animate():
    global spinner_index
    frame_path = os.path.join(image_folder, f'frame{spinner_index}.png')
    image = Image.open(frame_path)
    spinner_image = ImageTk.PhotoImage(image)
    
    spinner_label.config(image=spinner_image)
    spinner_label.image = spinner_image
    
    spinner_index = (spinner_index % 31) + 1 
    
    if spinner_index == 1:
        app.after(100, animate)
    else:
        app.after(100, animate)

app = tk.Tk()
app.title("YouTube MP3 Downloader")

url_label = ttk.Label(app, text="Enter the YouTube URL:")
url_entry = ttk.Entry(app, width=40)
download_button = ttk.Button(app, text="Download MP3", command=download_mp3)
status_label = ttk.Label(app, text="")

youtube_dl_path_label = ttk.Label(app, text="Current youtube-dl Path:")
youtube_dl_path_entry = ttk.Entry(app, width=40)
output_directory_label = ttk.Label(app, text="Current Output Directory:")
output_directory_entry = ttk.Entry(app, width=40)
set_paths_button = ttk.Button(app, text="Set Paths", command=set_custom_paths)

url_label.grid(row=0, column=0, padx=10, pady=10)
url_entry.grid(row=0, column=1, padx=10, pady=10)
download_button.grid(row=1, column=0, columnspan=2, padx=10, pady=10)
status_label.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

youtube_dl_path_label.grid(row=4, column=0, padx=10, pady=10)
youtube_dl_path_entry.grid(row=4, column=1, padx=10, pady=10)
output_directory_label.grid(row=5, column=0, padx=10, pady=10)
output_directory_entry.grid(row=5, column=1, padx=10, pady=10)
set_paths_button.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

youtube_dl_path_entry.insert(0, default_youtube_dl_path)
output_directory_entry.insert(0, default_output_directory)

app.mainloop()
