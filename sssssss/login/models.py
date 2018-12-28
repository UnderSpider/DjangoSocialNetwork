# login/models.py
from django.db import models


class User(models.Model):
    '''用户表'''

    gender = (
        ('male', '男'),
        ('female', '女'),
    )

    name = models.CharField(max_length=128, unique=True)
    password = models.CharField(max_length=256)
    email = models.EmailField(unique=True)
    sex = models.CharField(max_length=32, choices=gender, default='男')
    c_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['c_time']
        verbose_name = '用户'
        verbose_name_plural = '用户'

class Img(models.Model):
    img_url = models.ImageField(upload_to='img')  # upload_to指定图片上传的途径，如果不存在则自动创建
    name=models.CharField(max_length=128)
    dataTime=models.CharField(max_length=128)
    dianzans=models.IntegerField(default=0)
    comments=models.IntegerField(default=0)
class dianzan(models.Model):
    name=models.CharField(max_length=128)
    number=models.CharField(max_length=128)
    userid=models.IntegerField(default=0)
class comment(models.Model):
    name=models.CharField(max_length=128)
    text=models.TextField()
    dataTime=models.CharField(max_length=128)
    userid=models.IntegerField(default=0)
