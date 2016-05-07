from django.contrib import messages
from django.http import HttpResponse, HttpResponseNotFound, JsonResponse, HttpResponseRedirect
from django.shortcuts import render

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
            user = User.objects.create_user(email=email, password=password, location=location)
            send_welcome_mail(user)
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
                check_users_location(user, location)

                a = Analyzer(location)
                data = a.get_data()
                result = {'date': data['forecast'][1]['date'],'sunrise': data['forecast'][1]['sunrise_time'], 'sunset': data['forecast'][1]['sunset_time'],
                          'min': data['forecast'][1]['temperature_min'],
                          'max': data['forecast'][1]['temperature_max']}
                # return HttpResponse(a.build_url())
                return JsonResponse(result)
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
    Location.objects.change_location(user, loc)


def send_welcome_mail(user):
    message = 'Thanks for your interest in our app\n\nYour email: %s\nYour password: %s' % (
    str(user.email), str(user.password))
    m = MailManager(str(user.email), message)
    m.login_to_server()
    m.send_mail()
