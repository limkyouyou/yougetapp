import yt_dlp as youtube_dl

def get_ytinfo(url, format):
    file_info = {}

    with youtube_dl.YoutubeDL() as ydl:
        info = ydl.extract_info(url, download=False)
        
        file_info['title'] = info.get('title', None)
        file_info['thumbnail'] = info.get('thumbnail', None)
        file_info['uploader'] = info.get('uploader', None)

        if format == 'mp4':
            format_list = []
            formats = info.get('formats', info)
            for f in formats:
                resolution = f.get('height', False)
                if resolution and (resolution == 480 or resolution == 720 or resolution >= 1080):
                    format_id = f['format_id']
                    ext = f['ext']
                    vcodec = f['vcodec']
                    format_list.append((format_id, str(resolution), ext, vcodec))
            file_info['format_list'] = format_list

    return file_info