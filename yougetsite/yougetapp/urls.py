from django.urls import path
from . import views

app_name='yougetapp'

urlpatterns = [
    path('', views.UrlView.as_view(), name='ygurl'),
]