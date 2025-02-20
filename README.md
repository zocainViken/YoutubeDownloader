# Audio, Video and Subtitle Downloader

This Python project allows you to download YouTube videos, audio files, and subtitles while cleaning up subtitle files for easier reading.

## Features

- Download YouTube videos in the best available quality.

- Could also be used to download Video on other platforms like Dailymotion...

- Extract and download audio files in MP3 format.

- Fetch automatic or manual subtitles in your preferred language.

- Clean VTT subtitle files by removing timestamps, positions, and redundant lines.


## Usage

Clone this repository and navigate to the project folder.

```sh
git clone https://github.com/zocainViken/YoutubeDownloader.git
cd YoutubeDownloader
```
## Requirements

Make sure you have the required packages installed:
```sh
python -m pip install -r requirements.txt
```
Additionally, you may need FFmpeg for audio extraction:

```sh
sudo apt-get install ffmpeg  # For Linux
brew install ffmpeg           # For macOS
https://ffmpeg.org/download.html # for windows
```


Update the url and file paths as needed in the Python script.

## Run the script:
```sh
python downloader.py
```

Example
```python
url = "https://www.youtube.com/shorts/DGHT-GOARcI"
audio_output_path = "audio.mp3"
video_output_path = "video.mp4"
subtitle_output_path = "subtitles.srt"

# Download audio, video, and subtitles
download_audio(url, audio_output_path)
download_video(url, video_output_path)
download_subtitles(url, subtitle_output_path)

# Clean up subtitles
input_vtt = 'subtitles.fr.vtt'
output_vtt = 'fichier_nettoye.txt'
clean_vtt(input_vtt, output_vtt)
```
## Notes

- Ensure the YouTube URL is correct and publicly accessible.

- The subtitle language can be modified by changing the subtitleslangs option in the download_subtitles function.

- clean_vtt is optimized for VTT files but could be adjusted for other subtitle formats.

## Troubleshooting

- If the script fails to download the subtitles, the video might not have subtitles available. Check with the YouTube video page manually.

- Missing FFmpeg can cause audio extraction issues — make sure it's installed and in your PATH.

## License

This project is open-source and available under the MIT License.



