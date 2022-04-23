from django.db import models
import time,datetime
from django.utils import timezone
# Create your models here.

class food(models.Model):
    active_choice = ((0,"no serve"),(1,"serve"))
    category = models.CharField(max_length=100)
    name_food = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField()
    price = models.DecimalField(max_digits = 200,decimal_places = 2)
    active = models.IntegerField(choices=active_choice,default=1)
class cart(models.Model):
    active_choice = ((0,"no"),(1,"yes"))
    user_name = models.CharField(max_length=100)
    id_foods = models.TextField()
    bill_code = models.CharField(max_length=100,null=True)
    active = models.IntegerField(choices=active_choice,default=0) 
    date_created = models.TextField(default = datetime.datetime.now())
    address_ship = models.TextField(null = True)
    
    