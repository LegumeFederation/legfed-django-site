#-*- coding: utf-8 -*-

from django.shortcuts import render

from .models import Species
from resource_mgr.models import Resource

# Create your views here.
def index(request) :
    latest_species_list = Species.objects.all()
    latest_urls_list = []
    for sp in latest_species_list :
        resources_list = Resource.objects.filter(species__in = [ sp ])
        latest_urls_list.append(resources_list)

    latest_species_and_urls_list = zip(latest_species_list, latest_urls_list)
    context = {
        'latest_species_and_urls_list': latest_species_and_urls_list,
    }
    return render(request, 'species_mgr/index.html', context)

