from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class Users(AbstractUser):
    email = models.EmailField(unique=True)
    avatar = ProcessedImageField(upload_to='avatar',default='avatar/default.png', verbose_name='头像')
    reg_date=models.DateTimeField(auto_now_add=True) 
    admin = models.BooleanField(default=False) # a superuser
    
    posts=models.ForeignKey(Posts,on_delete=models.PROTECT)
    history=models.ForeignKey(Posts,on_delete=models.PROTECT)
    