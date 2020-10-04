from django.contrib import admin
from . import models

class MeasureAdmin(admin.ModelAdmin):
    readonly_fields = ('creation_date',)

admin.site.register(models.Measure, MeasureAdmin)