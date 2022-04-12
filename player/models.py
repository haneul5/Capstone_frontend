from django.db import models

# Create your models here.

from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=30)
    hook_text = models.CharField(max_length=100, blank=True) #요약문
    content = models.TextField()

    head_video = models.FileField(upload_to = "Uploaded Files/", blank=True, null=True)
    
    #file_upload = models.FileField(upload_to= 'player/files/%Y/%m/%d/', blank=True)
    created_at = models.DateTimeField(auto_now_add=True) #작성시간 = 현재시간 고정
    update_at = models.DateTimeField(auto_now=True) #얘로 업데이트 시간 ㅇㅇ

    def __str__(self):
        return f'[{self.pk}]{self.title}'

    def get_absolute_url(self):
        return f'/player/{self.pk}/'