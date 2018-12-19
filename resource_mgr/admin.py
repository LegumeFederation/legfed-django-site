from django.contrib import admin

# Register your models here.
from .models import Organization, Resource
from .models import DataDownload, Tour
from .models import Tool, ToolDataType, ToolAnalysisType

admin.site.register(Organization)
admin.site.register(Resource)

class DataDownloadAdmin(admin.ModelAdmin) :
    exclude = (
        'species',
    )

admin.site.register(DataDownload, DataDownloadAdmin)

class TourAdmin(admin.ModelAdmin) :
    exclude = (
        'species',
    )

admin.site.register(Tour, TourAdmin)

class ToolAdmin(admin.ModelAdmin) :
    exclude = (
        'species',
    )

admin.site.register(Tool, ToolAdmin)
admin.site.register(ToolDataType)
admin.site.register(ToolAnalysisType)

