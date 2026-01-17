import re
import yt_dlp
from pydub import AudioSegment
from mutagen.easyid3 import EasyID3
import os
import sys

def process(index: int) -> tuple[str, str]:
    arg = sys.argv[index]
    return re.sub(r"[<>:\"/\\|?*]", '_', arg), arg

url = sys.argv[1].split('&')[0] # remove query string
artist, artist_raw = process(2)
title, title_raw = process(3)
album, album_raw = process(4)
start = int(sys.argv[5])
end = int(sys.argv[6])

ydl_opts = {
    "js_runtimes" : {"node" : {}},
    "remote_components" : {"ejs:github" : {}},
    "format" : "bestaudio/best",
    "outtmpl" : f"[raw] {artist} - {title} ({album})",
    "postprocessors" : [
        {
            "key" : "FFmpegExtractAudio",
            "preferredcodec" : "mp3",
            "preferredquality" : "128"
        }
    ],
    "quiet" : True,
    "no_warnings" : True,
    "cookiefile" : "cookies.txt"
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl: # type: ignore
    ydl.download([url])

audio = AudioSegment.from_file(f"[raw] {artist} - {title} ({album}).mp3")

# pad starting
duration = len(audio)
if start < 0:
    audio = audio[-start*1000:]
elif start > 0:
    padding = AudioSegment.silent(duration = start*1000)
    audio = padding + audio

# pad ending
duration = len(audio)
if end < 0:
    audio = audio[:end*1000]
elif end > 0:
    padding = AudioSegment.silent(duration = end*1000)
    audio = audio + padding

# others
duration = len(audio)
audio = audio[:-(duration%1000)]
volume_change = -10 - audio.dBFS
audio = audio.apply_gain(volume_change)
audio.export(f"{artist} - {title} ({album}).mp3", format = "mp3", bitrate = "128k")

# Edit metadata / ID3 tags
EasyID3.RegisterTXXXKey("paddings", "PADDINGS")
EasyID3.RegisterTXXXKey("url", "URL")
audio = EasyID3(f"{artist} - {title} ({album}).mp3")
audio["artist"] = artist_raw
audio["title"] = title_raw
audio["album"] = album_raw
audio["paddings"] = [str(start), str(end)]
audio["url"] = url
audio.save()

os.remove(f"[raw] {artist} - {title} ({album}).mp3")
