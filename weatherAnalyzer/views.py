from django.http import HttpResponse, HttpResponseNotFound, JsonResponse, HttpResponseRedirect
from django.shortcuts import render
import pygeoip

from weatherAnalyzer.forms import LoginForm
from ipware.ip import get_real_ip, get_ip


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.authenticate()
            x_forwarded = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded:
                ip = x_forwarded.split(',')[0]
            else:
                ip = request.META.get('REMOTE_ADDR')
            ip = '78.141.68.228'
            gi = pygeoip.GeoIP('GeoLiteCity.dat', pygeoip.MEMORY_CACHE)
            location = gi.record_by_addr(ip)
            return HttpResponse('Your ip is: ' + ip + str(location))

    if request.method == 'GET':
        form = LoginForm()
    return render(request, 'weatherAnalyzer/login.html', {'form': form})
