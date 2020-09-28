from django.contrib import admin
from . import models

class UserAdmin(admin.ModelAdmin):
    readonly_fields = ('creation_date', 'update_date',)
    list_display = ('cedula', 'email', 'first_name', 'last_name', 'doctor', 'is_active')


admin.site.register(models.User, UserAdmin)