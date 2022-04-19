from tabnanny import verbose
from unicodedata import category
from django.db import models
from django.contrib.auth.models import User # 다대일 관계 구현
import os


#카테고리
class Category(models.Model):
    name = models.CharField(max_length=50, unique=True) #unique 트루는 카테고리 중복 안되게
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/player/category/{self.slug}/'

    class Meta:
        verbose_name_plural = 'Categories'

#포스트
class Post(models.Model):
    title = models.CharField(max_length=30)
    hook_text = models.CharField(max_length=100, blank=True) #요약문
    content = models.TextField()

    head_image = models.ImageField(upload_to = "Uploaded Files/", blank=True, null=True)
    head_video = models.FileField(upload_to = "Uploaded Files/", blank=True, null=True)
    
    #file_upload = models.FileField(upload_to= 'player/files/%Y/%m/%d/', blank=True)
    created_at = models.DateTimeField(auto_now_add=True) #작성시간 = 현재시간 고정
    update_at = models.DateTimeField(auto_now=True) #얘로 업데이트 시간 ㅇㅇ

    author = models.ForeignKey(User, on_delete=models.CASCADE) # 작성자가 삭제되면 해당 게시물도 다 삭제하게 함

    category = models.ForeignKey(Category, null = True, blank=True, on_delete=models.SET_NULL)
    def __str__(self):
        return f'[{self.pk}]{self.title}'

    def get_absolute_url(self):
        return f'/player/{self.pk}/'
