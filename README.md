# Download audio from YouTube with customizable adjustments

## Requirements

- FFmpeg
- Node.js
- cookies.txt (Use https://chrome.google.com/webstore/detail/get-cookiestxt-locally/cclelndahbckbenkjhflpdbgdldlbecc) (You may need to update frequently)

## Arguments

- Target URL
- Artist
- Title
- Album
- Seconds to pad before starting (negative value to trim)
- Seconds to pad after ending (negative value to trim)

## How To Run

- `git clone https://github.com/luihin903/YouTube-Audio-Downloader.git`
- `cd YouTube-Audio-Downloader`
- `python -m venv venv`
- `venv\Scripts\activate`
- `pip install -r requirements.txt`
- `python main.py [Target URL] [Artist] [Title] [Album] [Seconds after starts] [Seconds before ends]`

## How It Works

- Retrieve the audio from YouTube
- Pad/trim the beginning
- Pad/trim the ending
- Trim to the smaller second
- Normalize volume (across files)
- Edit metadata/tags
