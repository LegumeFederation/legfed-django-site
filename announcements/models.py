#-*- coding: utf-8 -*-

from django.db import models
from django.core.exceptions import ValidationError

class Announcement(models.Model) :
    description = models.CharField(max_length = 256)
    url = models.CharField(max_length = 256)
    location = models.CharField(max_length = 64, default = '')
    start_date = models.DateField()
    end_date = models.DateField()

    class Meta :
        ordering = [ 'end_date', 'start_date', 'description' ]

    def clean(self):
        if self.start_date > self.end_date :
            raise ValidationError("Start date is after end date")

    def __str__(self) :
        return '%s, %s'%(self.description, self.location)

