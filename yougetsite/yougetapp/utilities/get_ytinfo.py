import yt_dlp as youtube_dl

def get_ytinfo(url):
    file_info = {}

    with youtube_dl.YoutubeDL() as ydl:
        info = ydl.extract_info(url, download=False)
        
        file_info['title'] = info.get('title', None)
        file_info['thumbnail'] = info.get('thumbnail', None)
        file_info['uploader'] = info.get('uploader', None)

    return file_info