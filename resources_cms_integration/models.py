# -*- coding: utf-8 -*-

from django.db import models

# Create your models here.
from cms.models import CMSPlugin
from resource_mgr.models import Resource

class DataDownloadsPluginModel(CMSPlugin) :
    def get_data_downloads() :
        return Resource.objects.filter(is_data = True)

    def __str__(self) :
        return 'Data Downloads go here'

class ToursPluginModel(CMSPlugin) :
    def get_tours() :
        return Resource.objects.filter(is_tour = True)

    def __str__(self) :
        return 'Tours go here'

