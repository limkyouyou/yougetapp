from django.shortcuts import render
from django.views import View

from yougetapp.forms import UrlForm

# Create your views here.

class UrlView(View):
    def get(self, request):
        url_form = UrlForm()

        return render(request, 'yougetapp/yg_url.html', {'url_form': url_form})