# -*- coding: utf-8 -*-
import os.path
from datetime import datetime, timedelta

from django.http import HttpResponse, HttpResponseBadRequest
from django.template.defaultfilters import slugify
from django.utils import simplejson as json
from django.views.decorators.csrf import csrf_exempt

from bkpserver.models import Origin, BackupHistory, Transfer

from . import header, HEADER_CONFIG_FILE

#Registra a máquina remota no servidor
@csrf_exempt
def register(request):
    if request.method == 'POST':
        try:
            origin = Origin.objects.get(name=request.POST['origin_name'])
            #nome já existe, peça para tentar de novo com outro nome
            error = { 
                'error' : { 
                    'message' : u'Este nome já está cadastrado no sistema.' +
                                'Por favor, escolha um novo nome.', 
                } 
            }
            return HttpResponse(json.dumps(error), mimetype="text/javascript")
        except Origin.DoesNotExist:
            try:
                origin = Origin.objects.create(
                    name=request.POST['origin_name'],
                    sshkey=request.POST['origin_sshkey'],
                    slug=slugify(request.POST['origin_name']))
            except:
                error = { 'error' : { 'message' : u'Dados inválidos', } }
                return HttpResponse(json.dumps(error),
                                    mimetype="text/javascript")
        
        return HttpResponse(json.dumps(header(origin.name)),
                            mimetype="text/javascript")        
    return HttpResponseBadRequest()

#Responde ao pedido de cabeçalho
@csrf_exempt
def get_header(request):
    if request.method == 'GET':
        return HttpResponse(json.dumps(header(request.POST['origin_name'])),
                            mimetype="text/javascript")
    return HttpResponseBadRequest()


#Responde ao pedido de arquivo de configuração
@csrf_exempt
def config(request):
    if request.method == 'POST':
        config = []
        config.append(header(request.POST['origin_name']))
        transfers = Transfer.objects.get(
                       origin__name=request.POST['origin_name'])
        time = datetime.now()
        time -= timedelta(minutes=time.minute,
                          seconds=time.second,
                          microseconds=time.microseconds)
        for t in transfers:
            d = t.destination
            c = {
                'backup' : {
                    'nome_destino': d.name,
                    'destino': d.full_address,
                    'periodicidade': t.delta,
                    'primeiro_backup': str(time),
                }
            }
            config.append(c)
        cfg = json.dumps(config)
        f = open(header['header']['config_path'],'w')
        f.write(cfg + '\n')
        f.close()
        ok = {'OK' : 'OK'}
        return HttpResponse(json.dumps(ok), mimetype="text/javascript")
    return HttpResponseBadRequest()


#Recebe o log de uma transferência
@csrf_exempt
def post_log(request):
    if request.method == "POST":
        try:
            origin = Origin.objects.get(name=request.POST['origin_name'])
        except Origin.DoesNotExist:
            error = { 'error' : { 'message' : u'Dados inválidos', } }
            return HttpResponse(json.dumps(error), mimetype="text/javascript")
            
        BackupHistory.objects.create(
            origin=origin,
            dump_date=datetime(request.POST['dump_date']),
            files=request.POST['files'],
            destination=request.POST['destination'],
            successful = request.POST['successful']
        )
        ok = { 'OK' : 'OK'}
        return HttpResponse(json.dumps(ok), mimetype="text/javascript")
    return HttpResponseBadRequest()
