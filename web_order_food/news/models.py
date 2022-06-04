from django.db import models

# Create your models here.
class news(models.Model):
    title = models.TextField()
    context = models.TextField(blank=True)
    link_seemore = models.TextField()
    image_new = models.ImageField()
    
    def __str__(self):
        return self.title