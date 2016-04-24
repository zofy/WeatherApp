from django.contrib import messages
from django.http import HttpResponse, HttpResponseNotFound, JsonResponse, HttpResponseRedirect
from django.shortcuts import render
import pygeoip

from weatherAnalyzer.analyzer import Analyzer
from weatherAnalyzer.forms import LoginForm, SignUpForm
import geocoder

from weatherAnalyzer.models import User, Location
from weatherAnalyzer.sender import MailManager


def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            location = get_users_location(request)
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            User.objects.create_user(email=email, password=password, location=location)
            messages.info(request, 'Thanks for signing in!')
            messages.info(request, 'Now you can login.')
            return HttpResponseRedirect('/mbForecast/login/')
    elif request.method == 'GET':
        form = SignUpForm()

    return render(request, 'weatherAnalyzer/login.html',
                  {'form': form, 'url': 'weatherAnalyzer:signUp', 'button': 'Sign Up'})


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.authenticate()
            if user is not None:
                location = get_users_location(request)
                data = check_users_location(user, location)
                return HttpResponse(str(data['lat']) + ', ' + str(data['lng']) + ', ' + data['city'])
            else:
                messages.error(request, 'Invalid input, try again!')

    if request.method == 'GET':
        form = LoginForm()
    return render(request, 'weatherAnalyzer/login.html',
                  {'form': form, 'url': 'weatherAnalyzer:login', 'button': 'Login'})


def get_users_location(request):
    x_forwarded = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded:
        ip = x_forwarded.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    ip = '78.141.101.59'
    gi = geocoder.freegeoip(ip)
    return gi.json


def check_users_location(user, location):
    loc = {'lat': None, 'lng': None, 'city': None}
    for data in loc:
        if location.get(data) is not None:
            loc[data] = location[data]
    return Location.objects.change_location(user, loc)


def save_user_location(location):
    pass
