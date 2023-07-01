from django.contrib.auth.models import User
from rest_framework import serializers
from app.models import Contact, Wallpaper


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ('id',  'name', 'desc', 'date')

class WallpaperSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallpaper
        fields = ('id', 'title', 'category', 'brand', 'wallpaper_image', 'date')