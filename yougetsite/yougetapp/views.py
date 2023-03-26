from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import View
from django.conf import settings
from django.http import JsonResponse, HttpResponse

from .models import FileData, ExtType, AudioQuality, VideoQuality, SessionKey, DlData
from .forms import UrlForm, QualityForm
from .utilities.get_ytinfo import get_ytinfo
from .utilities.dl_ytfile import download_file
from .utilities.conf_title import conf_title

from pathlib import Path
from os import remove, listdir
import shutil

# Create your views here.

class UrlView(View):
    template = 'yougetapp/yg_url.html'
    def get(self, request):
        url_form = UrlForm()

        return render(request, self.template, {'url_form': url_form})
    
    def post (self, request):
        url_form = UrlForm(request.POST)
        if not url_form.is_valid():
            return render(request, self.template, {'url_form': url_form})
      
        valid_url = request.POST['url']
        format_type = request.POST['format_choice']

        file_info = get_ytinfo(valid_url, format_type)

        save_file_data, create = FileData.objects.get_or_create(
            url=valid_url,
            file_name=conf_title(file_info['title']),
            img_url=file_info['thumbnail'],
            uploader=file_info['uploader'],
        )

        if format_type == 'mp3':
            quality_list = [
                ('320', '320kpbs'),
                ('128', '128kpbs'),
            ]
            mime_type = 'audio/mpeg'
            save_ext_type, created = ExtType.objects.get_or_create(ext_name=format_type, mime_type=mime_type)
            for quality in quality_list:
                save_audio_quality, created = AudioQuality.objects.get_or_create(ext=save_ext_type, audio_quality=quality[0])
        elif format_type == 'mp4':
            available_quality_list = file_info['format_list']
            quality_list = []
            mime_type = 'video/mp4'
            save_ext_type, created = ExtType.objects.get_or_create(ext_name=format_type, mime_type=mime_type)
            for quality in available_quality_list:
                format_id, resolution, ext, vcodec = quality
                quality_list.append((f'{format_id},{resolution},{vcodec}', f'{ext}, {resolution}p, {vcodec}'))
                save_video_quality, crated = VideoQuality.objects.get_or_create(
                    ext=save_ext_type,
                    format_id=format_id,
                    resolution=resolution,
                    codec=vcodec,
                )
        request.session['quality_list'] = quality_list
        request.session['format'] = format_type

        return redirect(reverse('yougetapp:ygprocess', args=[save_file_data.pk]))
    
class ProcessView(View):
    def get(self, request, pk):
        active_file = get_object_or_404(FileData, id=pk)

        dl_file_objs = DlData.objects.filter(file_deleted=False)
        for obj in dl_file_objs:
            if not obj.was_downloaded_recently():
                file_dir = f'{settings.MEDIA_ROOT}/{obj.session.session_key}'
                file_path = Path(f'{file_dir}/{obj.file.file_name}-{str(obj.id)}.{obj.quality_object.ext.ext_name}')
                if file_path.exists():
                    remove(file_path)
                    obj.file_deleted = True
                    obj.save()
                if Path(file_dir).exists() and not listdir(file_dir):
                    shutil.rmtree(file_dir)

        quality_list = request.session['quality_list']
        if len(quality_list) == 0:
            ctx = {'no_quality': 'There are no available file in this format.'}
        else:
            quality_form = QualityForm(quality_list=quality_list)
            ctx = {'quality_form': quality_form}
        
        ctx['file_data'] = active_file
        ctx['title'] = active_file.file_name
        ctx['thumbnail'] = active_file.img_url
        ctx['uploader'] = active_file.uploader

        return render(request, 'yougetapp/yg_processed.html', ctx)
    
class PrepareDownload(View):
    def post(self, request, pk):
        active_file = get_object_or_404(FileData, id=pk)
        title = active_file.file_name
        url = active_file.url

        active_session, created = SessionKey.objects.get_or_create(session_key=request.session.session_key)

        active_format = get_object_or_404(ExtType, ext_name=request.session['format'])

        quality = request.POST['choice_list']
        if active_format.ext_name == 'mp3':
            format_id = quality
            quality_obj = get_object_or_404(AudioQuality, ext=active_format, audio_quality=format_id)
        elif active_format.ext_name == 'mp4':
            format_id, resolution, codec = quality.split(',')
            quality_obj = get_object_or_404(VideoQuality, ext=active_format, format_id=format_id, resolution=resolution, codec=codec)

        dl_file_data = DlData(
            file=active_file,
            session=active_session,
            quality_object=quality_obj,
        )
        dl_file_data.save()

        file_dir = settings.MEDIA_ROOT + active_session.session_key
        try:
            Path(file_dir).mkdir()
        except FileExistsError:
            pass
        
        download_file(title, url, file_dir, active_format.ext_name, format_id, str(dl_file_data.id))

        return JsonResponse(dl_file_data.pk, safe=False)

def user_download(requet, pk):
    dl_file_data = get_object_or_404(DlData, id=pk)
    file_session = dl_file_data.session.session_key
    file_dir = settings.MEDIA_ROOT +file_session
    format_type = dl_file_data.quality_object.ext.ext_name
    mime = dl_file_data.quality_object.ext.mime_type
    file_name = dl_file_data.file.file_name + '-' + str(dl_file_data.id) + '.' + format_type
    file_path = file_dir + '/' + file_name
    with open(file_path, 'rb') as file:
        response = HttpResponse(file, content_type=mime)
        response['Content-Disposition'] = f'attachement; filename="{file_name}"'
    
    return response