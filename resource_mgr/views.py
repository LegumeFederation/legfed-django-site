#-*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponseRedirect

from .models import Resource, Organization
from .models import DataDownload, Tour
from .models import Tool, ToolDataType

import json
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

def gwas(request) :
    if request.method == 'POST' :
        # Write the returned GWAS metadata to a file
        dout = '/var/www/legfed-django-site/legfedsite/ds-public/'
        obj = json.loads(request.POST.get('json'))
        fout = open(dout + obj['filename'] + '.json', 'w')
        fout.write(json.dumps(obj))
        fout.close()

        # Done - return to the Data Store page
        return HttpResponseRedirect("/resource_mgr/data/")

    context = {}
    return render(request, 'resource_mgr/data/gwas.html', context)

def tours(request) :
    tours_list = Tour.objects.all()
    context = {
        'tours_list': tours_list,
    }
    return render(request, 'resource_mgr/tours.html', context)

def tools(request) :
    tools_list = Tool.objects.all()
    datatypes_list = ToolDataType.objects.all()

    # construct the graph JSON
    nn = ','.join(['{"name":"%s","id":%d}'%(t.name, t.id) for t in datatypes_list])
    ll = ','.join(['{"name":"%s","source":%d,"target":%d}'%(t.get_text(), t.input_data_type.id, t.output_data_type.id) for t in tools_list])
    tools_graph_json = '{"nodes":[%s],"links":[%s]}'%(nn, ll)

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

