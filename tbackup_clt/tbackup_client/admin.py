# -*- coding: utf-8 -*-

import requests

from django.contrib import admin
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.utils import simplejson as json
        
from tbackup_client.models import Log, Config, Origin, Destination, WebServer
from tbackup_client.forms import ConfigForm, RegisterForm, LogForm

class ConfigAdmin(admin.ModelAdmin):
    form = ConfigForm

    def has_add_permission(self, request):
        return Origin.objects.filter(pk=1).exists()

    def has_delete_permission(self, request, obj=None):
        return Origin.objects.filter(pk=1).exists()
    
    def has_change_permission(self, request, obj=None):
        return Origin.objects.filter(pk=1).exists()

    def add_view(self, request, form_url='', extra_context=None):
        if request.method =='GET':
            self._retrieve_destinations()
        return super(ConfigAdmin, self).add_view(request, form_url, extra_context)
    
    def change_view(self, request,form_url=''):
        if request.method =='GET':
            self._retrieve_destinations()
        return super(ConfigAdmin, self).change_view(request,form_url)
    
    #quiet method to retrieve list of destinations from WebServer
    def _retrieve_destinations(self):
        ws = WebServer.objects.get(pk=1)
        url = ws.url + 'tbackup_server/retrieve/'
        response = requests.get(url, verify=False)
        if response.status_code == 200:
            for destination in json.loads(response.text):
                Destination.objects.get_or_create(name=destination)
        
admin.site.register(Config, ConfigAdmin)

class OriginAdmin(admin.ModelAdmin):
    form = RegisterForm

    add_form_template = 'admin/change_form.djhtml'
    change_form_template = 'admin/view_form.djhtml'
    
    def has_add_permission(self, request):
        return not Origin.objects.filter(pk=1).exists()

    def has_delete_permission(self, request, obj=None):
        return False
    
    def add_view(self, request, form_url='', extra_context=None):
        if request.method == 'GET':
            if not WebServer.objects.filter(pk=1).exists():
                from tbackup_client import webserver_fixture
                webserver_fixture.run()
        elif request.method == 'POST':
            from tbackup_client import crypt
            pvtkey, pubkey = crypt.generate_rsa_keys(1024)
            request.POST['pvtkey'] = pvtkey
            request.POST['pubkey'] = pubkey
        
            value = {
                'origin_name': request.POST['name'],
                'origin_pubkey': pubkey,
            }
            request_message = {
                'error' : False,
                'encrypted': False,
                'key': False,
                'value' : json.dumps(value),
            }

            #register client in webserver
            ws = WebServer.objects.get(pk=1)
            url = ws.url + 'tbackup_server/register/'
            response = requests.post(url, request_message, verify=False)
            
            if response.status_code != 200:
                return HttpResponse(content=response.text, content_type=response.headers['content-type'])
            
            response_text = json.loads(response.text)
            if response_text['error']:
                response_message = response_text['value']
                return render_to_response('register_msg.djhtml', { 'message' : response_message, })
            response_values = json.loads(response_text['value'])
            ws.pubkey=response_values['webserver_pubkey']
            ws.save()
            
        return super(OriginAdmin, self).add_view(request, form_url, extra_context)
    
admin.site.register(Origin, OriginAdmin)

class LogAdmin(admin.ModelAdmin):
    form = LogForm
    
    list_display = ('filename', 'date', 'destination', 'remote_status', 'restore_link')
    list_filter = ('destination', 'date', 'remote_status')
    search_fields = ['=filename', ]
    
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

#class RestoreAdmin(admin.AdminSite):
    
