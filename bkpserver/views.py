# -*- coding: utf-8 -*-
import os.path
import sys

from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.utils import simplejson

from bkpserver.models import Origin

projectdir = os.path.dirname(os.path.dirname(__file__)) + '/'
sys.path.insert(0,projectdir)
import settings

@csrf_exempt
def register(request):
    if request.method == POST:
        try:
            origin = Origin.objects.get(name=request.POST['name'])
            #nome já existe, peça para tentar de novo com outro nome
            error = {
                'ERROR' : {
                    'message' : u'Este nome já está cadastrado no sistema.',
                }
            }
            return HttpResponse(simplejson.dumps(error), mimetype="text/javascript")
        except Origin.DoesNotExist:
            origin = Origin.objects.create(
                name=request.POST['name'], 
                sshkey=request.POST['sshkey']
            )
        
        print origin.name
        print origin.sshkey
        origin.save()

        header = getattr(settings, 'HEADER_CONFIG_FILE')
        return HttpResponse(simplejson.dumps(header), mimetype="text/javascript")        
    return HttpResponseBadRequest()

@csrf_exempt
def get_header(request):
    if request.method == GET:
        header = getattr(settings, 'HEADER_CONFIG_FILE')
        return HttpResponse(simplejson.dumps(header), mimetype="text/javascript")
    return HttpResponseBadRequest()
    

#def get_config_file(request,machine_id):
#    if request.method == GET:
#        return render_to_response('transfer/index.html')

#def post_log(request, machine_hash):
#    if request.method == POST:
#        return render_to_response('transfer/index.html')
    
