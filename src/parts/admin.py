from django.contrib import admin

from .models import Part

class PartAdmin(admin.ModelAdmin):
    list_display = ('vin', 'name', 'code', 'count', 'unit')
    list_filter = ['vin']
    search_fields = ['vin']

admin.site.register(Part, PartAdmin)