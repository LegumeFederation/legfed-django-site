from django.db import models

# Create your models here.
# ----------------------------------------------------------

class LinkoutService(models.Model) :
    name = models.CharField(max_length = 255)
    url_format = models.CharField("URL Format", max_length = 255, help_text = 'Uses sprintf format, with all fields represented as %s')

    class Meta :
        ordering = [ 'name' ]

    def __str__(self) :
        return self.name

# ----------------------------------------------------------

class GeneLinkout(LinkoutService) :
    gene_example = models.CharField(max_length = 255)

    def insert_gene(self, gene) :
        return self.url_format%(gene)

    def example(self) :
        return self.insert_gene(self.gene_example)

# ----------------------------------------------------------

class GenomicRegionLinkout(LinkoutService) :
    sequence_example = models.CharField(max_length = 255)
    start_example = models.CharField(max_length = 12)
    end_example = models.CharField(max_length = 12)

    def insert_genomic_region(self, sequence_name, start, end) :
        return self.url_format%(sequence_name, start, end)

    def example(self) :
        return self.insert_genomic_region(self.sequence_example, self.start_example, self.end_example)

# ----------------------------------------------------------

