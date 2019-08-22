from django.db import models
from django.core.exceptions import ValidationError

import re
import requests

# Create your models here.
# ----------------------------------------------------------

class LinkoutService(models.Model) :
    name = models.CharField(max_length = 255)
    # url_format might look like 'https:/www.ncgr.org/species/$1/gene/$2/json'
    url_format = models.CharField("URL Format", max_length = 255, help_text = 'Represent fields as $1, $2, etc')
    # regex captures the fields to be inserted into url_format
    regex = models.CharField("Regular Expression", max_length = 255, default = '(.+)',
        help_text = 'Pattern of captures must match URL format') # '.+' matches any non-empty string
    # true_linkouts = True if URL returns linkouts that already exist, False if created on the fly
    true_linkouts = models.BooleanField("URL returns true linkouts", default = True,
        help_text = 'Uncheck to create pseudo-linkouts on the fly')

    class Meta :
        ordering = [ 'name' ]

    def num_fields_expected(self) :
        mm = re.findall('\$\d+', self.url_format)
        return len(mm)

    def clean(self) :
        nf_url = self.num_fields_expected()
        nf_captured = self.regex.count('(') - self.regex.count('\(') # for now

        if (nf_url == 0) :
            raise ValidationError('URL format must contain at least one field')
        elif (nf_captured == 0) :
            raise ValidationError('Regex must capture at least one field')
        # elif (nf_url < nf_captured) :
            # TODO: could regex have extra fields, unused by url_format?
            # raise ValidationError('URL format and regex must have the same number of fields')

    def __str__(self) :
        return self.name

class LinkoutException(Exception) :
    pass

# ----------------------------------------------------------

class GeneLinkout(LinkoutService) :
    gene_example = models.CharField(max_length = 255)

    def construct_url(self, gene) :
        rr = re.search(self.regex, gene)
        if rr is None :
            raise LinkoutException('Invalid gene name format: ' + gene)
        gg = rr.groups()
        if (len(gg) < self.num_fields_expected()) :
            raise LinkoutException('Wrong number of fields in gene name: ' + gene)
        # TODO: put fields in arbitrary order specified in url_format (like $2 $3 $1 $4)
        fmt = re.sub('\$\d+', '%s', self.url_format)
        return fmt % gg

    def get_linkouts(self, gene) :
        links_json = []

        try :
            url = self.construct_url(gene)
        except LinkoutException as e :
            # print(e) # TODO: could log the error,
            return links_json # but ignore it for now

        if self.true_linkouts :
            # service is a true linkout
            try :
                rr = requests.get(url)
                links_json = rr.json()
            except :
                pass # for now
        else :
            # service is a pseudo-linkout
            links_json.append({
                'href': url,
                'text': self.name
            })

        return links_json

    def get_example_linkouts(self) :
        return get_linkouts(self, self.gene_example)

# ----------------------------------------------------------

class GenomicRegionLinkout(LinkoutService) :
    sequence_example = models.CharField(max_length = 255)
    start_example = models.CharField(max_length = 12)
    end_example = models.CharField(max_length = 12)

    def construct_url(self, sequence_name, start, end) :
        rr = re.search(self.regex, sequence_name)
        if rr is None :
            raise LinkoutException('Invalid sequence name format: ' + sequence_name)
        gg = rr.groups()
        if (len(gg) < self.num_fields_expected() - 2) :
            raise LinkoutException('Wrong number of fields in sequence name: ' + sequence_name)
        # TODO: put fields in arbitrary order specified in url_format (like $2 $3 $1 $4)
        fmt = re.sub('\$\d+', '%s', self.url_format)
        return fmt % (gg + (start, end))

    def get_linkouts(self, sequence_name, start, end) :
        links_json = []

        try :
            url = self.construct_url(sequence_name, start, end)
        except LinkoutException as e :
            # print(e) # TODO: could log the error,
            return links_json # but ignore it for now

        if self.true_linkouts :
            # service is a true linkout
            try :
                rr = requests.get(url)
                links_json = rr.json()
            except :
                pass # for now
        else :
            # service is a pseudo-linkout
            links_json.append({
                'href': url,
                'text': self.name
            });

        return links_json

    def get_example_linkouts(self) :
        return get_linkouts(self, self.sequence_example, self.start_example, self.end_example)

# ----------------------------------------------------------

