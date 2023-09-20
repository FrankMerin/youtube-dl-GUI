# youtube-dl-applet (WINDOWS ONLY)

As this utalizes yt-dlp, it supports playlists (public/unlisted), and direct youtube links/share links

### _EXE_
The executable can be launched directly, download is located in \dist\
[Download Executable](https://github.com/FrankMerin/youtube-dl-applet/raw/main/dist/musicDL.exe)


## ✨_Usage (as exe):_✨

![Usage image](https://cdn.discordapp.com/attachments/280776371779928074/1153904262380789861/image.png)

### _Pre-Reqs (as code):_

youtube-dl - https://github.com/ytdl-org/youtube-dl

ffmpeg - https://ffmpeg.org/

#### _Launching for the first time (as code):_
Set the path to your youtube-dl.exe and the output folder you would like. 

Keep youtube-dl and ffmpeg in the same folder

#### _Set as windows shortcut (as code):_
To run this as a shortcut, create a shortcut, set the properties for "Target" to the following... (edit the path as needed)
C:\Users\{your_python_path}\AppData\Local\Programs\Python\Python310\python.exe C:\Users\{path_to_musictk}\Documents\applet\musictk.py

#### _Run manually (as code):_
open terminal... python musictk.py



## ✨_Usage (as code):_✨
![Launched image](https://cdn.discordapp.com/attachments/280776371779928074/1153069407027855390/image.png)

![Running image](https://cdn.discordapp.com/attachments/280776371779928074/1153068704100253767/image.png)

![Completed](https://cdn.discordapp.com/attachments/280776371779928074/1153069065703800933/image.png)

#### _Build on your own:_

download the build folder, add yt-dlp and ffmpeg to the folder, run the below command.

pyinstaller --onefile --name musicDL musicDL.py --add-binary "ffmpeg.exe;." --add-binary "yt-dlp.exe;." --add-data "loading.gif;." --add-data "helpersDL.py;."