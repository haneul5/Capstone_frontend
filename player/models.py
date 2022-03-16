from django.db import models

# Create your models here.

from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=30)
    content = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True) #작성시간 = 현재시간 고정
    update_at = models.DateTimeField(auto_now=True) #얘로 업데이트 시간 ㅇㅇ
    


    def __str__(self):
        return f'[{self.pk}]{self.title}'

    def get_absolute_url(self):
        return f'/player/{self.pk}/'