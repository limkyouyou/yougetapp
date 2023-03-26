import youtube_dl

def check_yturl(url):
    exts = youtube_dl.extractor.gen_extractors()
    for ext in exts:
        if ext.suitable(url) and ext.IE_NAME != 'generic':
            return True
    return False