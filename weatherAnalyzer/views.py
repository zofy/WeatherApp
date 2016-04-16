from django.http import HttpResponse, HttpResponseNotFound, JsonResponse, HttpResponseRedirect
from django.shortcuts import render
import pygeoip

from weatherAnalyzer.analyzer import Analyzer
from weatherAnalyzer.forms import LoginForm, SignUpForm
from ipware.ip import get_real_ip, get_ip

from weatherAnalyzer.models import User
from weatherAnalyzer.sender import MailManager


def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            location = get_users_location(request)
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            User.objects.create_user(email=email, password=password, location=location)
    elif request.method == 'GET':
        form = SignUpForm()

    return render(request, 'weatherAnalyzer/login.html',
                  {'form': form, 'url': 'weatherAnalyzer:signUp', 'button': 'Sign Up'})


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.authenticate()
            location = get_users_location(request)

            a = Analyzer(str(location.get('latitude')), str(location.get('longitude')))
            url = a.build_url()
            w_data = a.get_data()
            m = MailManager('zofy11@gmail.com', str(w_data))
            m.login_to_server()
            m.send_forecast()
            return HttpResponse(url)

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
    # ip = '78.141.68.228'
    gi = pygeoip.GeoIP('GeoLiteCity.dat', pygeoip.MEMORY_CACHE)
    return gi.record_by_addr(ip)


def save_user_location(location):
    pass
