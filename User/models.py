from django.db import models
from django.contrib.auth.models import AbstractUser
from Post.models import Post
from imagekit.models import ProcessedImageField
# Create your models here.

class User(AbstractUser):
    email = models.EmailField(unique=True)
    avatar = ProcessedImageField(upload_to='avatar',default='avatar/default.png', verbose_name='头像')
    reg_date=models.DateTimeField(auto_now_add=True) 
    admin = models.BooleanField(default=False) # a superuser
    

    