import yt_dlp as youtube_dl
import glob
import os

def download_file(title, url, dir, format, quality, id):
    file_dir = dir + '/' + title + '-' + id + '.%(ext)s'
    audio_quality = 'bestaudio/best'
    if format == 'mp3':
        ydl_opts = {
            'outtmpl': file_dir,
            'format': audio_quality,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': quality
            }],
        }
    elif format == 'mp4':
        ydl_opts = {
            'outtmpl': file_dir,
            'format': quality + '+' + audio_quality,
            'postprocessors': [{
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4',
            }],
        }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])