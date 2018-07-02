# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

from cms.models import CMSPlugin
from polls.models import Poll

class PollPluginModel(CMSPlugin):
    poll = models.ForeignKey(Poll)

    def __unicode__(self):
        return self.poll.question
