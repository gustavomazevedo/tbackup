# -*- coding: utf-8 -*-
import os.path
import sys

from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.utils import simplejson

from bkpserver.models import Origin

#projectdir = os.path.dirname(os.path.dirname(__file__)) + '/'
#sys.path.insert(0,projectdir)
from django.conf import settings

@csrf_exempt
def register(request):
    if request.method == 'POST':
        try:
            origin = Origin.objects.get(name=request.POST['name'])
            #nome já existe, peça para tentar de novo com outro nome
            error = { 'ERROR' : { 'message' : u'Este nome já está cadastrado no sistema.', } }
            return HttpResponse(simplejson.dumps(error), mimetype="text/javascript")
        except Origin.DoesNotExist:
            try:
                origin = Origin.objects.create(name=request.POST['name'],sshkey=request.POST['sshkey'])
            except:
                error = { 'ERROR' : { 'message' : u'Dados inválidos', } }
                return HttpResponse(simplejson.dumps(error), mimetype="text/javascript")
        
        print origin.name
        print origin.sshkey
        origin.save()

        header = getattr(settings, 'HEADER_CONFIG_FILE')
        header['header']['config_path'] = header['header']['config_path'].replace('{origin_name}',origin_name)
        return HttpResponse(simplejson.dumps(header), mimetype="text/javascript")        
    return HttpResponseBadRequest()

@csrf_exempt
def get_header(request):
    if request.method == 'GET':
        return HttpResponse(simplejson.dumps(header(origin_name)), mimetype="text/javascript")
    return HttpResponseBadRequest()

def header(origin_name):
    h = getattr(settings, 'HEADER_CONFIG_FILE')
    return h['header']['config_path'].replace('{origin_name}',origin_name)

@csrf_exempt
def config(request):
    if request.method == 'POST':
        config = []
        header = getattr(settings, 'HEADER_CONFIG_FILE')
        header['header']['config_path'] = header['header']['config_path'].replace('{origin_name}',origin_name)
        config.append(header)
        tranfers = Transfer.objects.get(origin__name=request.POST['origin_name'])
        time = datetime.now()
        time -= timedelta(minutes=time.minute, seconds=time.second, microseconds=time.microseconds)
        for t in transfers:
            d = t.destination
            c = {
                'backup' : {
                    'nome_destino': d.name,
                    'destino': d.full_address,
                    'periodicidade': parse_delta(t.delta),
                    'primeiro_backup': str(time),
                }
            }
            config.append(c)
        cf = simplejson.dumps(config)
        f = open(header['header']['config_path'],'w')
        f.write(cf + '\n')
        f.close()
        return render_to_response('transfer/index.html')
    return HttpResponseBadRequest()

#def post_log(request, machine_hash):
#    if request.method == POST:
#        return render_to_response('transfer/index.html')
    
