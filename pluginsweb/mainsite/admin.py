from django.contrib import admin
from models import Plugin


class PluginAdmin(admin.ModelAdmin):
    list_display = ('name', 'version', 'uploaded')
    list_filter = ('uploaded', )
    search_fields = ('name', 'description')


admin.site.register(Plugin, PluginAdmin)


