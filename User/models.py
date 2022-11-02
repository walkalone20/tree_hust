from django.db import models
from django.contrib.auth.models import AbstractUser
from Post.models import Post
from imagekit.models import ProcessedImageField
# Create your models here.

class User(AbstractUser):
    email = models.EmailField(unique=True,verbose_name='邮箱')
    

    