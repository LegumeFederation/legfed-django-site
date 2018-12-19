from django.db import models
from filer.fields.image import FilerImageField
from species_mgr.models import Species

# ----------------------------------------------------------

class Organization(models.Model) :
    name = models.CharField(max_length = 128)
    url = models.CharField(max_length = 256, null = True, blank = True)
    contact_email = models.CharField(max_length = 64, null = True, blank = True)
    icon = FilerImageField(null = True, blank = True, related_name = 'Organization_icons')

    class Meta :
        ordering = [ 'name' ]

    def __str__(self) :
        return self.name

# ----------------------------------------------------------

class Resource(models.Model) :
    org = models.ForeignKey(Organization, verbose_name = 'organization that provides it', on_delete = models.CASCADE)
    url = models.CharField(max_length = 256)
    text = models.CharField('Text (if different from Organization)', max_length = 256, null = True, blank = True)
    hints = models.CharField(max_length = 64, null = True, blank = True)
    species = models.ManyToManyField(Species, verbose_name = 'its related species', blank = True)

    class Meta :
        # order by org in order to group by org
        ordering = [ 'org', 'text' ]

    def get_text(self) :
        text = self.text
        if (text is None) :
            text = self.org.name
        return text

    def __str__(self) :
        if (hasattr(self, 'datadownload')) :
            text = '[DATA DOWNLOAD] ' + self.get_text()
        elif (hasattr(self, 'tool')) :
            text = '[TOOL] ' + self.get_text()
        elif (hasattr(self, 'tour')) :
            text = '[TOUR] ' + self.get_text()
        else :
            text = self.get_text()

        if (not(self.species is None or len(self.species.all()) == 0)) :
            ss = ', '.join(sp.get_abbreviation() for sp in self.species.all())
            text += ' (%s)'%(ss)

        return text

# ----------------------------------------------------------

class DataDownload(Resource) :
    species = None

    def __str__(self) :
        return self.get_text()

class Tour(Resource) :
    species = None

    def __str__(self) :
        return self.get_text()

# ----------------------------------------------------------

class ToolDataType(models.Model) :
    name = models.CharField(max_length = 255)

    class Meta :
        ordering = [ 'name' ]

    def __str__(self) :
        return self.name

class ToolAnalysisType(models.Model) :
    name = models.CharField(max_length = 255)

    class Meta :
        ordering = [ 'name' ]

    def __str__(self) :
        return self.name

class Tool(Resource) :
    species = None
    input_data_type = models.ForeignKey(ToolDataType, related_name = 'tool_input_data_type', on_delete = models.CASCADE)
    output_data_type = models.ForeignKey(ToolDataType, related_name = 'tool_output_data_type', on_delete = models.CASCADE)
    analysis_type = models.ForeignKey(ToolAnalysisType, on_delete = models.CASCADE)

    class Meta :
        # for now, order by analysis_type in order to group by analysis_type
        ordering = [ 'analysis_type', 'text' ]

    def get_text(self) :
        text = self.text
        if (text is None) :
            text = self.url
        return text

    def __str__(self) :
        return self.get_text()

# ----------------------------------------------------------

