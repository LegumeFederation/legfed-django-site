#-*- coding: utf-8 -*-

from django.shortcuts import render

from .models import Resource, Organization
from .models import DataDownload, Tour

# Create your views here.
def index(request) :
    context = {}
    return render(request, 'resource_mgr/index.html', context)

def data(request) :
    data_downloads_list = DataDownload.objects.all()
    context = {
        'data_downloads_list': data_downloads_list,
    }
    return render(request, 'resource_mgr/data.html', context)

def tours(request) :
    tours_list = Tour.objects.all()
    context = {
        'tours_list': tours_list,
    }
    return render(request, 'resource_mgr/tours.html', context)

def organizations(request) :
    orgs_list = Organization.objects.all()
    context = {
        'orgs_list': orgs_list,
    }
    return render(request, 'resource_mgr/organizations.html', context)

