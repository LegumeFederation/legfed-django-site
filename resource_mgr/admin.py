from django.contrib import admin

# Register your models here.
from .models import Organization, Resource
admin.site.register(Organization)
admin.site.register(Resource)

