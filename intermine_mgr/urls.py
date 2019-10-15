#-*- coding: utf-8 -*-

from django.conf.urls import url
from . import views

app_name = "intermine_mgr"
urlpatterns = [
    url(r'^$', views.index, name = 'index'),
    url(r'^templates/$', views.templates, name = 'templates'),
    url(r'^templates/constraints/$', views.template_constraints, name = 'constraints'),
]
