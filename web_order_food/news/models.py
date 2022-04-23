from django.db import models

# Create your models here.
class news(models.Model):
    title = models.TextField()
    context = models.TextField(blank=True)
    test_vui = models.TextField(blank=True)