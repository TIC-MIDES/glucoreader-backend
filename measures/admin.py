from django.contrib import admin
from . import models

class MeasureAdmin(admin.ModelAdmin):
    readonly_fields = ('creation_date', 'value',)
    list_display = ('patient', 'creation_date', 'value')


admin.site.register(models.Measure, MeasureAdmin)