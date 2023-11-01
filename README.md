# youtube-dl GUI (WINDOWS ONLY)

=====================NOTE!!!!=====================

WINDOWS RECOGNIZES THE EXE AS Trojan:Win32/Wacatac.B!ml

Unfortunately, I can't do much about it.
The exe that gets created is not machine code. It is a package of a python interpreter and the code. The interpreter portion of the code is always found in (written in python) malware. So machine learning models used in AV are likely to pick it up as malicious.

You will need to manually whitelist the application to use it.

===================================================

As this utalizes yt-dlp, it supports playlists (public/unlisted), and direct youtube links/share links

## ✨_Usage:_✨

Download the binary from the [releases page](https://github.com/FrankMerin/youtube-dl-applet/releases/).

[Direct download](https://github.com/FrankMerin/youtube-dl-applet/releases/download/latest/musicDL.exe)

![Usage image](https://cdn.discordapp.com/attachments/280776371779928074/1156418796874117130/image.png)

### _Pre-Reqs (for building):_

ffmpeg - https://ffmpeg.org/

Save ffmpeg.exe to the src folder


#### _Build on your own:_

After cloning, add ffmpeg to the src folder, run the below command.

```ps1
powershell.exe -File .\build.ps1
```