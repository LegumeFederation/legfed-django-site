#-*- coding: utf-8 -*-

from django.conf.urls import url
from . import views

app_name = "announcements"
urlpatterns = [
    url(r'^$', views.index, name = 'index'),
    url(r'^past/$', views.past, name = 'past'),
]

