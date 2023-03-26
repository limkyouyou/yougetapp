from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import View

from .models import FileData, ExtType, AudioQuality, VideoQuality
from .forms import UrlForm, QualityForm
from .utilities.get_ytinfo import get_ytinfo

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
            file_name=file_info['title'],
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
                quality_list.append((format_id, f'{ext}, {resolution}p, {vcodec}'))
                save_video_quality, crated = VideoQuality.objects.get_or_create(
                    ext=save_ext_type,
                    format_id=format_id,
                    resolution=resolution,
                    codec=vcodec,
                )
        request.session['quality_list'] = quality_list

        return redirect(reverse('yougetapp:ygprocess', args=[save_file_data.pk]))
    
class ProcessView(View):
    def get(self, request, pk):
        active_file = get_object_or_404(FileData, id=pk)

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