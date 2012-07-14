# -*- coding: utf-8 -*-

from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response
from bkpserver.models import Client


OK = 0

@csrf_exempt
def register(request):
    if request.method == POST:
        try:
            client = Client.objects.get(name=request.POST['name'])
            #nome já existe, peça para tentar de novo com outro nome
            return HttpResponse()
        except Sistema.DoesNotExist:
            client = Client.objects.create(name=request.POST['name'])
        
        client.sshkey = request.POST['sshkey']    
        return OK
    return render_to_response()

#def get_config_file(request,machine_id):
#    if request.method == GET:
#        return render_to_response('transfer/index.html')

#def post_log(request, machine_hash):
#    if request.method == POST:
#        return render_to_response('transfer/index.html')
    
