from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class Users(AbstractUser):
    nickname = models.CharField(max_length=30, blank=True, null=True, verbose_name='昵称')
    password = models.CharField(max_length=15,verbose_name='密码')
    avatar = ProcessedImageField(upload_to='avatar',default='avatar/default.png', verbose_name='头像')
    email = models.EmailField(unique=True)
    reg_date=models.DateTimeField(auto_now_add=True) 
    auth = models.IntegerField()
    
    posts=models.ForeignKey(Posts,on_delete=models.PROTECT)
    history=models.ForeignKey(Posts,on_delete=models.PROTECT)
    