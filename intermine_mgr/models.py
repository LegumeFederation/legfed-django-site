from django.db import models

# Create your models here.
class InterMine(models.Model) :
    name = models.CharField("Name", max_length = 64)
    url = models.CharField("URL", max_length = 255)

    class Meta :
        ordering = [ 'name' ]
        verbose_name_plural = 'InterMines'

    def __str__(self) :
        return self.name

