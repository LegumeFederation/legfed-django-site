from django.db import models
from species_mgr.models import Species

class Organization(models.Model) :
    name = models.CharField(max_length = 128)

    class Meta :
        ordering = [ 'name' ]

    def __str__(self) :
        return self.name

class Resource(models.Model) :
    org = models.ForeignKey(Organization, verbose_name = 'organization that provides it', on_delete = models.CASCADE)
    species = models.ManyToManyField(Species, verbose_name = 'its related species')
    text = models.CharField('Text (if different from Organization)', max_length = 256, null = True, blank = True)
    url = models.CharField(max_length = 256)

    class Meta :
        # order by org in order to group by org
        ordering = [ 'org', 'text' ]

    def get_text(self) :
        text = self.text
        if (text is None) :
            text = self.org.name
        return text

    def __str__(self) :
        ss = ', '.join(sp.get_abbreviation() for sp in self.species.all())
        return self.get_text() + ' (%s)'%(ss)

