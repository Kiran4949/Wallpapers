from django.db import models
from statistics import mode
from django.contrib.auth.models import User


# Create your models here.

class Contact(models.Model):
    name = models.CharField(max_length=122)
    email = models.CharField(max_length=122)
    desc = models.TextField()
    date = models.DateField()

    def __str__(self):
        return self.name


CATEGORY_CHOICE = (
    ('N', 'Nature'),
    ('S', 'Space'),
    ('CO', 'Country'),
    ('A', 'Animal'),
    ('T', 'Tajmahal'),
    ('C', 'Car'),
    ('F', 'Flower'),
    ('W', 'Window'),
    ('CA', 'Cartoon'),
    ('M', 'Mobile'), 
    ('TO', 'Top'),   
)

class Wallpaper(models.Model):
    title = models.CharField(max_length=255)
    category = models.CharField(choices=CATEGORY_CHOICE, max_length=5, default=CATEGORY_CHOICE)
    brand = models.CharField(max_length=255, default='New')
    wallpaper_image = models.ImageField(upload_to='wallpaperimg')
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)

    
