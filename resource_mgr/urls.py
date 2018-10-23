#-*- coding: utf-8 -*-

from django.conf.urls import url
from . import views

app_name = "resource_mgr"
urlpatterns = [
    url(r'^$', views.index, name = 'index'),
    url(r'^data/$', views.data, name = 'data'),
    url(r'^tours/$', views.tours, name = 'tours'),
]

