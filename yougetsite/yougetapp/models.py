from django.db import models
from django.utils import timezone
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType

import datetime
# Create your models here.

class DlData(models.Model):
    file = models.ForeignKey('FileData', on_delete=models.CASCADE)
    session = models.ForeignKey('SessionKey', on_delete=models.CASCADE)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    quality_object = GenericForeignKey('content_type', 'object_id')

    file_deleted = models.BooleanField(default=False)
    downloaded_at = models.DateTimeField(auto_now_add=True)

    def was_downloaded_recently(self):
        return self.downloaded_at >= timezone.now() - datetime.timedelta(minutes=5)
    
    def __str__(self):
        return f'{self.file.file_name} downloaded at {self.downloaded_at.strftime("%Y-%m-%d-%H:%M:%S")}'

class FileData(models.Model):
    url = models.URLField(max_length=200)
    file_name = models.CharField(max_length=100)
    img_url = models.CharField(max_length=200, null=True)
    uploader = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.file_name} by {self.uploader}'
    
class SessionKey(models.Model):
    session_key = models.CharField(max_length=130)

    def __str__(self):
        return self.session_key
    
class ExtType(models.Model):
    ext_name = models.CharField(max_length=3)
    mime_type = models.CharField(max_length=15)

    def __str__(self):
        return self.ext_name
        
class VideoQuality(models.Model):
    ext = models.ForeignKey('ExtType', on_delete=models.CASCADE)

    format_id = models.CharField(max_length=3)
    resolution = models.CharField(max_length=4, null=True)
    codec = models.CharField(max_length=50, null=True)

    dl_data = GenericRelation(DlData, null=True)

    def __str__(self):
        return f'{self.format_id}, {self.resolution}p, {self.codec}'
        
class AudioQuality(models.Model):
    ext = models.ForeignKey('ExtType', on_delete=models.CASCADE)

    audio_quality = models.CharField(max_length=4)

    dl_data = GenericRelation(DlData, null=True)

    def __str__(self):
        return f'{self.audio_quality}kbps'