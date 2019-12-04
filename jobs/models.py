from django.db import models

# Create your models here.
from django.core.exceptions import ValidationError

class Job(models.Model) :
    job_title = models.CharField(max_length = 256)
    institution = models.CharField(max_length = 256)
    brief_description = models.CharField(max_length = 256)
    url = models.CharField(max_length = 256)
    post_date = models.DateField()
    expiration_date = models.DateField()
    filled = models.BooleanField()

    class Meta :
        ordering = [ '-expiration_date', '-post_date', 'institution', 'job_title' ]

    def clean(self):
        if self.post_date > self.expiration_date :
            raise ValidationError("Post date is after expiration date")

    def __str__(self) :
        return '%s, %s'%(self.job_title, self.institution)

