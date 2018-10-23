# -*- coding: utf-8 -*-

from django.db import models

# Create your models here.
from cms.models import CMSPlugin
from species_mgr.models import Species
from resource_mgr.models import Resource

class SpeciesPluginModel(CMSPlugin) :
    def get_species_with_resources() :
        species_list = Species.objects.all()
        urls_list = []
        for sp in species_list :
            resources_list = Resource.objects.filter(species__in = [ sp ])
            urls_list.append(resources_list)

        species_and_urls_list = zip(species_list, urls_list)
        return species_and_urls_list

    def __str__(self) :
        return 'Species go here'

