from django.conf.urls import url

from . import views

app_name='weatherAnalyzer'

urlpatterns = [
    # url(r'^new$', views.new, name='newUser'),
    # url(r'^(?P<id>d*)/$', views.show, name='showUser'),
    url(r'^signUp/$', views.sign_up, name='signUp'),
    url(r'^login/$', views.login, name='login'),
    # url(r'^signUp$', views.signUp, name='signUp'),
]