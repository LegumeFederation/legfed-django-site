#-*- coding: utf-8 -*-

from django.conf.urls import url
from . import views

app_name = "resource_mgr"
urlpatterns = [
    url(r'^$', views.index, name = 'index'),
    url(r'^data/$', views.data, name = 'data'),
    url(r'^data/gwas/$', views.gwas, name = 'gwas'),
    url(r'^tours/$', views.tours, name = 'tours'),
    url(r'^tools/$', views.tools, name = 'tools'),
    url(r'^organizations/$', views.organizations, name = 'organizations'),
]

