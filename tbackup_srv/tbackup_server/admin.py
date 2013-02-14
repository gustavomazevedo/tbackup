# -*- coding: utf-8 -*-

from django.contrib import admin

from tbackup_server.models import Log, Destination
from tbackup_server.forms import LogForm

admin.site.register(Destination)

class LogAdmin(admin.ModelAdmin):
    form = LogForm
    
    list_display = ('origin', 'destination', 'filename', 'date', 'status')
    list_filter = ('origin', 'destination', 'date', 'status')
    search_fields = ['=filename', '=origin', '=destination', '=date']
    
    change_form_template = 'admin/view_form.djhtml'
    actions = None
    
    fieldsets = [
        (None, {'fields':()}), 
        ]

    def __init__(self, *args, **kwargs):
        super(LogAdmin, self).__init__(*args, **kwargs)
        self.list_display_links = (None, )
        
    def has_add_permission(self, request):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False
    
    def change_view(self, request, form_url='', extra_context=None):
        pass
    
    def save_model(self):
        pass
    
admin.site.register(Log, LogAdmin)