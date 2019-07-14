from django.contrib import admin

# Register your models here.
from .models import GeneLinkout, GenomicRegionLinkout

admin.site.register(GeneLinkout)
admin.site.register(GenomicRegionLinkout)

