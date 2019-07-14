from django.db import models

# Create your models here.
class IntermineService(models.Model) :
    name = models.CharField("Name", max_length = 64)
    url = models.CharField("URL", max_length = 255)

    def insert_keyword(self, keyword) :
        return '%s/%s'%(self.url, keyword)

    def __str__(self) :
        return self.name

