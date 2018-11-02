#-*- coding: utf-8 -*-

from django.shortcuts import render

from .models import Resource, Organization

# Create your views here.
def index(request) :
    context = {}
    return render(request, 'resource_mgr/index.html', context)

def data(request) :
    data_downloads_list = Resource.objects.filter(is_data = True)
    context = {
        'data_downloads_list': data_downloads_list,
    }
    return render(request, 'resource_mgr/data.html', context)

def tours(request) :
    tours_list = Resource.objects.filter(is_tour = True)
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

