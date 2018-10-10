#-*- coding: utf-8 -*-

from django.db import models
from filer.fields.image import FilerImageField

class Species(models.Model) :
    genus_name = models.CharField(max_length = 32)
    species_name = models.CharField(max_length = 32)
    common_name = models.CharField(max_length = 64)
    icon = FilerImageField(null = True, blank = True, related_name = 'species_icons')

    class Meta :
        ordering = [ 'genus_name', 'species_name', 'common_name' ]
        verbose_name_plural = 'Species'

    def to_gggss(self) :
        return '%s%s'%(self.genus_name[0:3], self.species_name[0:2])

    def __str__(self) :
        return '%s %s (%s)'%(self.genus_name, self.species_name, self.common_name)

