from django.conf.urls import include, url
from django.contrib import admin
from django.shortcuts import render


urlpatterns = [
    url(r'^$', lambda request: render(request, 'home.html')),
    #  url(r'^', include('myapp.urls')),
    url(r'^admin/', admin.site.urls),
]
