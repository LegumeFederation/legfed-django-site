# -*- coding: utf-8 -*-

from django.db import models

# Create your models here.
from cms.models import CMSPlugin
from announcements.models import Announcement
from datetime import date

class AnnouncementPluginModel(CMSPlugin) :
    def get_announcements() :
        return Announcement.objects.filter(end_date__gte = date.today())

    def __str__(self) :
        return 'Announcements go here'

