from django.db import models
import time,datetime
from django.utils import timezone
# Create your models here.
class category(models.Model):
    category = models.CharField(max_length=100)
    def __str__(self):
        return self.category
class food(models.Model):
    active_choice = ((0,"no serve"),(1,"serve"))
    category_food = models.ForeignKey(category, on_delete=models.CASCADE)
    name_food = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField()
    price = models.DecimalField(max_digits = 200,decimal_places = 2)
    active = models.IntegerField(choices=active_choice,default=1)

    def __str__(self):
        return self.name_food
class cart(models.Model):
    active_choice = ((0,"no"),(1,"yes"))
    statement_bill_choice = ((0,"pending"),(1,"delivering"),(2,"delivered"))
    user_name = models.CharField(max_length=100)
    id_foods = models.TextField()
    bill_code = models.CharField(max_length=100,null=True)
    active = models.IntegerField(choices=active_choice,default=0)
    date_created = models.DateTimeField(auto_now_add=True)
    address_ship = models.TextField(null = True)
    number_telephone = models.TextField(blank=True)
    receiver = models.TextField(null = True)
    coupon_code = models.CharField(max_length=20,default = "100")
    raw_price = models.TextField(max_length=100)
    final_price = models.TextField(max_length=100,null=True)
    statement_bill = models.IntegerField(choices = statement_bill_choice,default = 0)
    paid_bill = models.BooleanField(default = False)

