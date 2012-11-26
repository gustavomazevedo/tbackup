# -*- coding: utf-8 -*-


from django.contrib import admin

from tbackup_client.models import Config

class ConfigAdmin(admin.ModelAdmin):
    fields=['destination', 'interval']
    
admin.site.register(Config, ConfigAdmin)