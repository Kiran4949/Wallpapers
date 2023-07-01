from django.urls import path, include
from app.api import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('users', views.UserViewSet, basename='users'),
router.register('contact', views.ContactViewSet, basename='contact'),
router.register('wallpapers', views.WallpaperViewSet, basename='wallapaprs')

urlpatterns = [
    path('', include(router.urls)),
]
