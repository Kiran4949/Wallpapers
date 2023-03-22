from django.contrib import admin
from app.models import Contact
from .models import (
    Wallpaper

)

# Register your models here.

admin.site.register(Contact)


@admin.register(Wallpaper)
class WallpaperModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'category', 'brand', 'wallpaper_image', 'date']
