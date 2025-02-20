import re
import yt_dlp
import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading

def clean_vtt(input_vtt, output_txt):
    with open(input_vtt, 'r', encoding='utf-8') as file:
        content = file.readlines()

    # Remove the first 3 lines
    content = content[3:]

    # Join remaining lines into a single text
    content = ''.join(content)

    # Remove time tags (e.g., 00:00:00.199 --> 00:00:03.889)
    content_no_time = re.sub(r'\d{2}:\d{2}:\d{2}\.\d{3} --> \d{2}:\d{2}:\d{2}\.\d{3}', '', content)

    # Remove position tags (e.g., align:start position:0%)
    content_no_position = re.sub(r'align:[^ \n]+ position:[^ \n]+', '', content_no_time)

    # Remove style tags (e.g., <c>text</c>)
    content_no_style = re.sub(r'<[^>]+>', '', content_no_position)

    # Clean up unnecessary line breaks
    content_cleaned = re.sub(r'\n+', '\n', content_no_style).strip()

    # Remove duplicate lines
    lines = content_cleaned.split('\n')
    lines_no_duplicates = list(dict.fromkeys(lines))

    # Remove lines without text (empty or just spaces)
    filtered_lines = [line for line in lines_no_duplicates if line.strip() != '']

    # Join filtered lines back together
    filtered_content = '\n'.join(filtered_lines)

    # Save the cleaned content to a text file
    with open(output_txt, 'w', encoding='utf-8') as file:
        file.write(filtered_content)

def download_video(url, output_path):
    def run():
        try:
            progress.start()
            ydl_opts = {
                'format': 'bestvideo+bestaudio/best',
                'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
                'merge_output_format': 'mp4',
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            messagebox.showinfo("Success", "Video download complete!")
        except Exception as e:
            messagebox.showerror("Error", f"Error downloading video: {e}")
        finally:
            progress.stop()

    threading.Thread(target=run).start()

def download_audio(url, output_path):
    def run():
        try:
            progress.start()
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            messagebox.showinfo("Success", "Audio download complete!")
        except Exception as e:
            messagebox.showerror("Error", f"Error downloading audio: {e}")
        finally:
            progress.stop()

    threading.Thread(target=run).start()

def download_subtitles(url, output_path):
    def run():
        try:
            progress.start()

            ydl_opts = {
                'skip_download': True,
                'writesubtitles': True,
                'writeautomaticsub': True,
                'subtitleslangs': ['fr', 'en'],
                'subtitlesformat': 'vtt',
                'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                if not info.get('subtitles') and not info.get('automatic_captions'):
                    messagebox.showerror("Error", "No subtitles available for this video.")
                    return
                ydl.download([url])

                # Find the downloaded VTT file
                video_title = info['title']
                subtitle_file = os.path.join(output_path, f"{video_title}.{ydl_opts['subtitleslangs'][0]}.vtt")
                cleaned_subtitle_file = os.path.join(output_path, f"{video_title}_{ydl_opts['subtitleslangs'][0]}_cleaned.txt")
                subtitle_file = os.path.join(output_path, f"{video_title}.{ydl_opts['subtitleslangs'][1]}.vtt")
                cleaned_subtitle_file = os.path.join(output_path, f"{video_title}_{ydl_opts['subtitleslangs'][1]}_cleaned.txt")

                if not os.path.exists(subtitle_file):
                    messagebox.showerror("Error", "Subtitle file was not found.")
                    return

                clean_vtt(subtitle_file, cleaned_subtitle_file)
                messagebox.showinfo("Success", f"Subtitles downloaded and cleaned successfully: {cleaned_subtitle_file}")
        except Exception as e:
            messagebox.showerror("Error", f"Error downloading subtitles: {e}")
        finally:
            progress.stop()

    threading.Thread(target=run).start()

def browse_folder():
    folder_selected = filedialog.askdirectory()
    folder_entry.delete(0, tk.END)
    folder_entry.insert(0, folder_selected)

# GUI Setup
root = tk.Tk()
root.title("YouTube Video Downloader")

# URL Input
tk.Label(root, text="YouTube URL:").pack(pady=5)
url_entry = tk.Entry(root, width=50)
url_entry.pack(pady=5)

# Folder Selection
folder_frame = tk.Frame(root)
folder_frame.pack(pady=5)
folder_entry = tk.Entry(folder_frame, width=50)
folder_entry.pack(side=tk.LEFT, padx=(0, 5))
browse_button = tk.Button(folder_frame, text="Browse", command=browse_folder)
browse_button.pack(side=tk.RIGHT)

# Download Buttons
tk.Button(root, text="Download Video", command=lambda: download_video(url_entry.get(), folder_entry.get())).pack(pady=5)
tk.Button(root, text="Download Audio", command=lambda: download_audio(url_entry.get(), folder_entry.get())).pack(pady=5)
tk.Button(root, text="Download Subtitles", command=lambda: download_subtitles(url_entry.get(), folder_entry.get())).pack(pady=5)

# Progress Bar
progress = ttk.Progressbar(root, orient="horizontal", length=300, mode="indeterminate")
progress.pack(pady=10)

root.mainloop()
