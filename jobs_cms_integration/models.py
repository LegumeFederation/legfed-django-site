from django.db import models

# Create your models here.
from cms.models import CMSPlugin
from jobs.models import Job
from datetime import date

class JobsPluginModel(CMSPlugin) :
    def get_jobs() :
        return Job.objects.filter(post_date__lte = date.today()).filter(expiration_date__gte = date.today()).filter(filled = False)

    def __str__(self) :
        return 'Jobs go here'

