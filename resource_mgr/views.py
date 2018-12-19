#-*- coding: utf-8 -*-

from django.shortcuts import render

from .models import Resource, Organization
from .models import DataDownload, Tour, Tool

import math

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

def tools(request) :
    tools_list = Tool.objects.all()

    # construct the graph JSON
    ll = ','.join(['{"source":%d,"target":%d}'%(t.input_data_type.id, t.output_data_type.id) for t in tools_list])
    nn = set()
    for t in tools_list :
        i = t.input_data_type.id
        o = t.output_data_type.id
        nn.update([i, o])
    n = max(nn)
    W = H = 480 # for now
    M = 10
    nn_xy = ','.join(['{"x":%d,"y":%d}'%(int(0.5*(W + (W - 2*M)*math.cos(2*math.pi*k/n))), int(0.5*(H + (H - 2*M)*math.sin(2*math.pi*k/n)))) for k in range(0, n) ]) # circular layout, for now
    tools_graph_json = '{"nodes":[%s],"links":[%s]}'%(nn_xy, ll)

    context = {
        'tools_list': tools_list,
        'tools_graph_json': tools_graph_json,
    }
    return render(request, 'resource_mgr/tools.html', context)

def organizations(request) :
    orgs_list = Organization.objects.all()
    context = {
        'orgs_list': orgs_list,
    }
    return render(request, 'resource_mgr/organizations.html', context)

