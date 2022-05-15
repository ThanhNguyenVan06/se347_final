from django.db import models

# Create your models here.
class discounts(models.Model):
    title = models.CharField(max_length=20)
    percent = models.DecimalField(max_digits = 5,decimal_places = 2)
    image_discount = models.ImageField()
    def __str__(self):
        return self.title