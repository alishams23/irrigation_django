from django.db import models
from django.core.validators import FileExtensionValidator

# Create your models here.
import os

def file_upload_path(instance, filename):

    
    # Combine folder name with the filename
    return os.path.join('videos', filename)

class Video(models.Model):
    image = models.ImageField(verbose_name="عکس")
    
    title = models.CharField(max_length=40)
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="زمان ساخنه شده")
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name="زمان بروز رسانی")


    video = models.FileField(upload_to=file_upload_path,null=True,
    validators=[FileExtensionValidator(allowed_extensions=['MOV','avi','mp4','webm','mkv'])])   

    def __str__(self):
        return F"{self.title}"

    class Meta:
        verbose_name = "فیلم"
        verbose_name_plural = "فیلم ها"
    

