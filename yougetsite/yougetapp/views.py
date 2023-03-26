from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import View

from .models import FileData
from .forms import UrlForm
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

        file_info = get_ytinfo(valid_url)

        save_file_data, create = FileData.objects.get_or_create(
            url=valid_url,
            file_name=file_info['title'],
            img_url=file_info['thumbnail'],
            uploader=file_info['uploader'],
        )

        return redirect(reverse('yougetapp:ygprocess', args=[save_file_data.pk]))
    
class ProcessView(View):
    def get(self, request, pk):
        active_file = get_object_or_404(FileData, id=pk)

        ctx = {
            'url': active_file.url,
            'title': active_file.file_name,
            'thumbnail': active_file.img_url,
            'uploader': active_file.uploader,
        }

        return render(request, 'yougetapp/yg_processed.html', ctx)