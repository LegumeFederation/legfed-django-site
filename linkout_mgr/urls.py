#-*- coding: utf-8 -*-

from django.conf.urls import url
from . import views

app_name = "linkout_mgr"
urlpatterns = [
    url(r'^$', views.index, name = 'index'),
    url(r'^test/$', views.test, name = 'test'),
]
