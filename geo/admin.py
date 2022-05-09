from django.contrib import admin
from leaflet.admin import LeafletGeoAdmin
from .models import Field, Soil, Research, Culture, FitoScan, AOI, Indexes, Farmer
# Register your models here.


class IndexesInline(admin.StackedInline):
    model = Indexes
    can_delete = False
    verbose_name_plural = 'Indexes'


class FitoScanInline(admin.StackedInline):
    model = FitoScan
    can_delete = False
    verbose_name_plural = 'FitoScan'


class ResearchAdmin(LeafletGeoAdmin):
    inlines = (IndexesInline, FitoScanInline)


admin.site.register(Farmer)
admin.site.register(Culture)
admin.site.register(Soil)
admin.site.register(Field, LeafletGeoAdmin)
admin.site.register(Research, ResearchAdmin)
admin.site.register(FitoScan, LeafletGeoAdmin)
admin.site.register(AOI, LeafletGeoAdmin)
admin.site.register(Indexes)
