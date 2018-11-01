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
    url = models.CharField(max_length = 256)
    text = models.CharField('Text (if different from Organization)', max_length = 256, null = True, blank = True)
    hints = models.CharField(max_length = 64, null = True, blank = True)
    species = models.ManyToManyField(Species, verbose_name = 'its related species', blank = True)
    is_data = models.BooleanField('Data Download', default = False)
    is_tour = models.BooleanField('Tour', default = False)

    class Meta :
        # order by org in order to group by org
        ordering = [ 'org', 'text' ]

    def get_text(self) :
        text = self.text
        if (text is None) :
            text = self.org.name
        return text

    def clean(self):
        if (not self.is_tour) :
            self.hints = None

    def __str__(self) :
        text = self.get_text()

        if (len(self.species.all()) > 0) :
            ss = ', '.join(sp.get_abbreviation() for sp in self.species.all())
            text += ' (%s)'%(ss)

        if (self.is_data) :
            text += ' (DATA DOWNLOAD)'

        if (self.is_tour) :
            text += ' (TOURS)'

        return text

