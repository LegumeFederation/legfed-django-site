# -*- coding: utf-8 -*-

from django.db import models

# Create your models here.
from cms.models import CMSPlugin
from resource_mgr.models import DataDownload, Tour

class DataDownloadsPluginModel(CMSPlugin) :
    def get_data_downloads() :
        return DataDownload.objects.all()

    def __str__(self) :
        return 'Data Downloads go here'

class ToursPluginModel(CMSPlugin) :
    def get_tours() :
        return Tour.objects.all()

    def __str__(self) :
        return 'Tours go here'

