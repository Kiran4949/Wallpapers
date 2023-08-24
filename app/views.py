from django.shortcuts import redirect, render
from datetime import datetime
from app.models import Contact
from django.views import View
from app.models import Wallpaper
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import EmailMessage, send_mail
from Wallpaper import settings
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from . tokens import generate_token
from django.db.models import Q
import json
import requests
from .config import RECAPTCHA_SECRET_KEY



# Create your views here.


def index(request):
    return render(request, 'index.html')


def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        # Recaptcha
        clientkey = request.POST.get('g-recaptcha-response')
        secretkey = RECAPTCHA_SECRET_KEY
        captchaData = {
            'secret': secretkey,
            'response': clientkey
        }
        r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=captchaData)
        response = json.loads(r.text)
        verify = response['success']  
        if verify:
            if User.objects.filter(username=username):
                messages.error(
                    request, "Username already exist! Please try some other username.")
                return redirect('home')

            if User.objects.filter(email=email).exists():
                messages.error(request, "Email Already Registered!!")
                return redirect('home')

            if len(username) > 20:
                messages.error(request, "Username must be under 20 charcters!!")
                return redirect('home')

            if pass1 != pass2:
                messages.error(request, "Passwords didn't matched!!")
                return redirect('home')

            if not username.isalnum():
                messages.error(request, "Username must be Alpha-Numeric!!")
                return redirect('home')

            myuser = User.objects.create_user(username, email, pass1)
            myuser.first_name = fname
            myuser.last_name = lname
            myuser.is_active = False
            myuser.save()
            messages.success(
                request, "Your Account has been created successfully!! Please check your email to confirm your email address in order to activate your account.")

            # Welcome Email  ( Its an 1st mail )
            subject = "Welcome to WALLPAPERs!!"
            message = "Hello " + myuser.first_name + "!!\n" + \
                "Welcome to WALLPAPERs!!\nThank you for visiting our website.\nWe have also sent you a confirmation email, please confirm your email address.\nThank You,\nTeam WALLPAPERs"
            from_email = settings.EMAIL_HOST_USER
            to_list = [myuser.email]
            send_mail(subject, message, from_email, to_list, fail_silently=True)

            # Email Address Confirmation Email   ( Its an 2nd mail )
            current_site = get_current_site(request)
            email_subject = "Confirm your Email @ WALLPAPERs - Login!!"
            message2 = render_to_string('email_confirmation.html', {

                'name': myuser.first_name,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
                'token': generate_token.make_token(myuser)
            })
            email = EmailMessage(
                email_subject,
                message2,
                settings.EMAIL_HOST_USER,
                [myuser.email],
            )
            email.fail_silently = True
            email.send()

            return redirect('login')

    return render(request, "signup.html")


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        myuser = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        myuser = None

    if myuser is not None and generate_token.check_token(myuser, token):
        myuser.is_active = True
        myuser.save()
        login(request, myuser)
        messages.success(request, "Your Account has been activated!!")
        return redirect('login')
    else:
        return render(request, 'activation_failed.html')



def loginUser(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username, password)
        # Recaptcha
        clientkey = request.POST.get('g-recaptcha-response')
        secretkey = RECAPTCHA_SECRET_KEY
        captchaData = {
            'secret': secretkey,
            'response': clientkey
        }
        r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=captchaData)
        response = json.loads(r.text)
        verify = response['success']  
        if verify:
            # Check if user has entered correct credentials.
            user = authenticate(username=username, password=password)
            if user is not None:
                # A backend authenticated the credentials
                login(request, user)
                return redirect("/")
            else:
                # No backend authenticated the credentials
                return render(request, 'login.html', {'error_message': 'Invalid username or password'})

    return render(request, 'login.html')


def contact(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        desc = request.POST.get('desc')
        # Recaptcha
        clientkey = request.POST.get('g-recaptcha-response')
        secretkey = RECAPTCHA_SECRET_KEY
        captchaData = {
            'secret': secretkey,
            'response': clientkey
        }
        r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=captchaData)
        response = json.loads(r.text)
        verify = response.get('success', False)
        if verify:
            contact = Contact(name=name, email=email, desc=desc, date=datetime.today())
            contact.save()
            messages.success(request, 'Your message has been sent!')
        else:
            messages.error(request, 'reCAPTCHA verification failed. Please try again.')

    return render(request, 'contact.html')



def about(request):
    return render(request, 'about.html')


class WallpaperDetailView(View):
    def get(self, request, pk):
        wallpaper = Wallpaper.objects.get(pk=pk)

        return render(request, 'wallpaperDetail.html', {'wallpaper': wallpaper})


class Nature(View):
    def get(self, request):
        natures = Wallpaper.objects.filter(category='N')

        return render(request, 'nature.html', {'natures': natures})


class Space(View):
    def get(self, request):
        spaces = Wallpaper.objects.filter(category='S')

        return render(request, 'space.html', {'spaces': spaces})


class Country(View):
    def get(self, request):
        countrys = Wallpaper.objects.filter(category='CO')

        return render(request, 'country.html', {'countrys': countrys})


class Animal(View):
    def get(self, request):
        animals = Wallpaper.objects.filter(category='A')

        return render(request, 'animal.html', {'animals': animals})


class Tajmahal(View):
    def get(self, request):
        tajmahals = Wallpaper.objects.filter(category='T')

        return render(request, 'tajmahal.html', {'tajmahals': tajmahals})


class Car(View):
    def get(self, request):
        cars = Wallpaper.objects.filter(category='C')

        return render(request, 'car.html', {'cars': cars})


class Flower(View):
    def get(self, request):
        flowers = Wallpaper.objects.filter(category='F')

        return render(request, 'flowers.html', {'flowers': flowers})


class Window(View):
    def get(self, request):
        windows = Wallpaper.objects.filter(category='W')

        return render(request, 'windows.html', {'windows': windows})


class Cartoon(View):
    def get(self, request):
        cartoons = Wallpaper.objects.filter(category='CA')

        return render(request, 'cartoons.html', {'cartoons': cartoons})


class Mobile(View):
    def get(self, request):
        mobiles = Wallpaper.objects.filter(category='M')

        return render(request, 'mobile.html', {'mobiles': mobiles})


def search(request):
    query = request.GET.get('search', '')  
    # Create Q objects for searching different fields
    brand_q = Q(brand__icontains=query)
    title_q = Q(title__icontains=query)
    category_q = Q(category__icontains=query)
    resolution_q = Q(resolution__icontains=query)
    # Combine the Q objects using the OR operator
    combined_q = brand_q | title_q | category_q | resolution_q
    wallpaper = Wallpaper.objects.filter(combined_q)

    return render(request, 'search.html', {'wallpaper': wallpaper})

