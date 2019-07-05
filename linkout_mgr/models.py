from django.db import models

# Create your models here.
class LinkoutService(models.Model) :
    url_prefix = models.CharField("URL Prefix", max_length = 255)
    gene_example = models.CharField(max_length = 255)
    url_suffix = models.CharField("URL Suffix", max_length = 255)

    class Meta :
        ordering = [ 'url_prefix', 'url_suffix' ]

    def insert_gene(self, gene) :
        return '%s/%s/%s'%(self.url_prefix, gene, self.url_suffix)

    def __str__(self) :
        return self.insert_gene(self.gene_example)

