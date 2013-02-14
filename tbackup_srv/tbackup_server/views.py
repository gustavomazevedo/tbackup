# -*- coding: utf-8 -*-

#import os.path

#import bz2
#
#
#from datetime import datetime, timedelta
#
from django.http import HttpResponse, HttpResponseBadRequest
from django.utils import simplejson as json
from django.views.decorators.csrf import csrf_exempt

from tbackup_server.models import Origin, Destination, WebServer, Log
from tbackup_server.api import json_view
from tbackup_server.handlers import exception_handler

def enum(*sequential, **named):
    enums = dict(zip(sequential, range(len(sequential))), **named)
    return type('Enum', (), enums)

err_codes = enum('DESTINATION_DOES_NOT_EXIST',
                 'MALFORMED_POST',
                 'NOT_ALLOWED',
                 'ORIGIN_ALREADY_EXISTS',
                 'ORIGIN_DOES_NOT_EXIST',
                 'SHA1SUM_MATCH_ERROR',
                 )

def index(request):
    from django.shortcuts import Http404
    raise Http404

@json_view
@exception_handler
@csrf_exempt
def name_available(request):
    if request.is_ajax():
        try:
            Origin.objects.get(name=request.POST['origin_name'])
            return False
        except Origin.DoesNotExist:
            return True
    return HttpResponseBadRequest()

#Registra a máquina remota no servidor
@json_view
@exception_handler
@csrf_exempt
def register(request):
    if request.method == 'POST':
        import logging
        
        if not 'value' in request.POST:
            return error(err_codes.MALFORMED_POST)
        
        request_values = json.loads(request.POST['value'])
        
        if not (all(k in request_values for k in ('origin_name', 'origin_pubkey'))):
            return error(err_codes.MALFORMED_POST)
    
        try:
            Origin.objects.get(name=request_values['origin_name'])
            return error(err_codes.ORIGIN_ALREADY_EXISTS)
        except Origin.DoesNotExist:
            Origin.objects.create(
                name=request_values['origin_name'],
                pubkey=request_values['origin_pubkey'])
            
            ws = get_or_create_webserver()
            server_info = {'webserver_name' : ws.name,
                           'webserver_pubkey' : ws.pubkey,
                           'webserver_newurl' : ws.url}
            message = {'error' : False, 
                       'value' : json.dumps(server_info)}
            
            logging.warning('server: criado com sucesso!')

        return message        
    return HttpResponseBadRequest()

@json_view
@exception_handler
@csrf_exempt
def retrieve(request):
    if request.method == 'GET':
        list_dests = list(Destination.objects.values_list('name', flat=True))
        return list_dests
    return HttpResponseBadRequest()    

@json_view
@exception_handler   
@csrf_exempt
def public_key(request):
    if request.method == 'GET':
        ws = get_or_create_webserver()
        return { 'webserver_pubkey' : ws.pubkey }

@json_view
@exception_handler
@csrf_exempt
def backup(request):
    if request.method == 'POST':
        import logging
        import os
        from os import path
        from base64 import b64decode
        from Crypto.Cipher import AES
        from Crypto.Hash import SHA
        from Crypto.PublicKey import RSA
        
        if not 'value' in request.POST:
            return error(err_codes.MALFORMED_POST)
        
        request_values = json.loads(request.POST['value'])
        
        if not (all(k in request_values for k in ('origin_name',
                                                  'origin_pubkey',
                                                  'destination',
                                                  'date',
                                                  'file_sha1sum',
                                                  'file_key'))):
            return error(err_codes.MALFORMED_POST)
        
        if not 'file' in request.FILES:
            return error(err_codes.NO_FILE_PROVIDED)
        
        try:
            Origin.objects.get(pubkey=request.POST['origin_pubkey'])
        except Origin.DoesNotExist:
            return error(err_codes.ORIGIN_DOES_NOT_EXIST)
        
        try:
            destination = Destination.objects.get(name=request_values['destination'])
        except Destination.DoesNotExist:
            return error(err_codes.DESTINATION_DOES_NOT_EXIST)
        
        logging.warning(destination.name)
         
        date = request_values['date']
        sha1sum_client = request_values['file_sha1sum']
        b64decodedAESkey = b64decode(request_values['file_key'])

        ws = get_webserver()
        rsa = RSA.importKey(ws.pvtkey)
        AESkey = rsa.decrypt(b64decodedAESkey)
        
        sha1 = SHA.new()
        
        filename = request.FILES['file'].name
        tmp_path = path.join(path.dirname(path.abspath(__file__)),filename.replace('.txt','b3.txt'))
        if path.exists(tmp_path):
            os.remove(tmp_path)
        i=0
        with open(tmp_path, 'wb+') as f:
            for chunk in request.FILES['file'].chunks():
                logging.warning('chunk %i' %i)
                i+=1
                f.write(chunk)
        with open(tmp_path, 'rb') as f:
            with open(tmp_path.replace('b3.','3.'), 'wb+') as g:
                counter = f.read(16)
                AESdecryptor = AES.new(AESkey, AES.MODE_CTR, counter=lambda: counter)
                for data in iter(lambda: f.read(64 * 1024)):
                    decypheredData = AESdecryptor.decrypt(data)
                    sha1.update(decypheredData)
                    g.write(decypheredData)
                
        sha1sum_server = sha1.hexdigest()
        logging.warning(sha1sum_client)
        logging.warning(sha1sum_server)
        
        if sha1sum_client != sha1sum_server:
            return error(err_codes.SHA1SUM_MATCH_ERROR)
        
        origin_name = request_values['origin_name']
        
        message = send_to_destination(request.FILES['file'], origin_name, destination, date, sha1sum_client)
        
        return message
    return HttpResponseBadRequest()


@exception_handler
@csrf_exempt
def restore(request):
    if request.method == 'POST':
        from django.core.servers.basehttp import FileWrapper
        import os.path
        
        request_values = json.loads(request.POST['value'])
        filename = request_values['filename']
        destination = request_values['destination']
        origin_name = request_values['origin_name']
        
        filepath = retrieve_from_destination(filename, origin_name, destination)
        wrapper = FileWrapper(file(filepath))
        response = HttpResponse(wrapper, content_type='text/plain')
        response['Content-Length'] = os.path.getsize(filepath)
        print response
        return response
    
    return HttpResponseBadRequest()

def get_sha1sum(string_data):
    #from hashlib import sha1
    #import cStringIO
    from Crypto.Hash import SHA
    sha1 = SHA.new()
    #s.update()
    #sha1 = sha1();
    #if isinstance(large_string, file):
    #    for data in iter(lambda: fileref.read(8192), b''):
    sha1.update(string_data)
    return sha1.hexdigest()

def send_to_destination(file_content, origin_name, destination, date, sha1sum):
    import logging
    dest = Destination.objects.get(name=destination) #sempre existirá
    logging.warning(dest)
    if dest.islocal:
        from os import path, makedirs
        directory = path.join(dest.address,origin_name)
        if not path.exists(directory):
            makedirs(directory)
            logging.warning('caminho criado')
        with open(path.join(directory,file_content.name), 'wb') as f:
            for chunk in file_content.chunks():
                f.write(chunk)
        o = Origin.objects.get(name=origin_name)
        from datetime import datetime
        Log.objects.create(origin=o,
                           destination=destination,
                           filename=file_content.name,
                           date=datetime.strptime(date, '%Y-%m-%d %H:%M:%S.%f'),
                           status=True)
        return {'success' : {'message' : u'Sucesso.',}}
    else:
        return {'error' : {'message' : u'Não implementado.',}}

def retrieve_from_destination(filename, origin_name, destination):
    dest = Destination.objects.get(name=destination)
    if dest.islocal:
        import os.path
        filepath = os.path.join(os.path.join(dest.address,origin_name),filename)
        if os.path.exists(filepath):
            return filepath
            

def error(code):
    if code == err_codes.DESTINATION_DOES_NOT_EXIST:
        msg = u'O destino informado não está cadastrado no sistema'
    elif code == err_codes.MALFORMED_POST:
        msg = u'POST estruturado incorretamente. Favor consultar documentação da API'
    elif code == err_codes.NO_FILE_PROVIDED:
        msg = u'Arquivo necessário não foi recebido'
    elif code == err_codes.ORIGIN_ALREADY_EXISTS:
        msg = u'Nome de origem já cadastrado'
    elif code == err_codes.ORIGIN_DOES_NOT_EXIST:
        msg = u'Origem informada não está cadastrada no sistema ou sua chave pública foi alterada'
    elif code == err_codes.SHA1SUM_MATCH_ERROR:
        msg = u'Arquivo corrompido durante transferência'
    
    return { 'error' : {'message' : msg,}}

def get_or_create_webserver():
    try:
        return get_webserver()
    except WebServer.DoesNotExist:
        return create_webserver()

def get_webserver():
    return WebServer.objects.get(id=1)

def create_webserver():
    from Crypto.PublicKey import RSA
    ws = WebServer.objects.create(name='SERVIDOR GRUYERE', 
                                  #url='https://gruyere.lps.ufrj.br/~gustavo/tbackup_server/')
                                  url='http://127.0.0.1:8080/')
    private = RSA.generate(1024)
    public = private.publickey()
    ws.pvtkey = private.exportKey()
    ws.pubkey = public.exportKey()
    ws.save()
    return ws    
