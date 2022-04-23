from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
# Create your models here.
class user(models.Model):
    fullname = models.CharField(max_length=255,default = '')
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    address = models.TextField(default='')    
    def __str__(self):
        return self.user.username
    