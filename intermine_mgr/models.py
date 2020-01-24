from django.db import models
from species_mgr.models import Species

# Create your models here.
class InterMine(models.Model) :
    name = models.CharField("Name", max_length = 64)
    url = models.CharField("URL", max_length = 255)
    species = models.ManyToManyField(Species, verbose_name = 'species with FASTA/BLAST sequences', blank = True)

    class Meta :
        ordering = [ 'name' ]
        verbose_name_plural = 'InterMines'

    def __str__(self) :
        return self.name

