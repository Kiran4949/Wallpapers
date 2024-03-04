from django.urls import include, path, re_path
from app import views
from django.contrib.auth import views as auth_views
from .forms import MyPasswordResetForm, MySetPasswordForm
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='home'),
    
    path('api/', include('app.api.urls')),

    path('about/', views.about, name="about"),

    path('contact/', views.contact, name="contact"),

    path('signup/', views.signup, name='signup'),

    path('activate/<uidb64>/<token>', views.activate, name='activate'),

    path('login/', views.loginUser, name="login"),

    path('login/login', views.loginUser, name="login"),

    path('password_reset/login', views.loginUser, name="login"),

    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),

    path('wallpaper-detail/logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    
    path('login/password_reset', auth_views.PasswordResetView.as_view(template_name='password_reset.html', form_class=MyPasswordResetForm), name='password_reset'),
    
    path('password_reset/done', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    
    path('password_reset_confirm/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html', form_class=MySetPasswordForm), name='password_reset_confirm'),
    
    path('password_reset_complete', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),
    
    path('wallpaper-detail/<int:pk>', views.WallpaperDetailView.as_view(), name='wallpaper-detail'),

    path('nature/', views.Nature.as_view(), name='nature'),

    path('space/', views.Space.as_view(), name='space'),

    path('country/', views.Country.as_view(), name='country'),

    path('animal/', views.Animal.as_view(), name='animal'),

    path('tajmahal/', views.Tajmahal.as_view(), name='tajmahal'),

    path('car/', views.Car.as_view(), name='car'),

    path('flower/', views.Flower.as_view(), name='flower'),

    path('windows/', views.Window.as_view(), name='windows'),

    path('cartoon/', views.Cartoon.as_view(), name='cartoon'),

    path('mobile/', views.Mobile.as_view(), name='mobile'),

    path('search/', views.search, name="search"),

    path('<category>/', views.dynamic_category, name='dynamic_category'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  

