# -*- coding: utf-8 -*-

#import os.path

#import bz2
#
#
#from datetime import datetime, timedelta
#
from django.http import HttpResponse, HttpResponseBadRequest
#from django.template.defaultfilters import slugify
#from django.utils import simplejson as json
from django.views.decorators.csrf import csrf_exempt
#
from tbackup_server.models import Origin, Destination, WebServer, Log

#from . import header, HEADER_CONFIG_FILE

NOT_ALLOWED = 0
SHA1SUM_MATCH_ERROR = 1

def index(request):
    from django.shortcuts import Http404
    raise Http404

@csrf_exempt
def name_available(request):
    if request.is_ajax():
        try:
            Origin.objects.get(name=request.POST['origin_name'])
            return HttpResponse('false', mimetype="text/javascript")
        except Origin.DoesNotExist:
            return HttpResponse('true', mimetype="text/javascript")
    return HttpResponseBadRequest()

#Registra a máquina remota no servidor
@csrf_exempt
def register(request):
    print 'server: recebi request.'
    if request.method == 'POST':
        #print 'server: é um POST'
        from django.utils import simplejson as json
        try:
            #print 'server: criando origin...'
            #print request.POST
            request_values = json.loads(request.POST['value'])
            #print request_values
            #print 'server: name %s' % request_values['origin_name']
            #print 'server: pubkey %s' % request_values['origin_pubkey']
            Origin.objects.create(
                name=request_values['origin_name'],
                pubkey=request_values['origin_pubkey'])
            #print 'server: cadastrou no banco'
            webserver_pubkey, webserver_url = get_webserver_pubkey_and_url()
            #print 'server: cadastrou webserver'
            #print 'server: server_pubkey %s' % webserver_pubkey
            server_info = {'webserver_name' : 'SERVIDOR GRUYERE',
                           'webserver_pubkey' : webserver_pubkey,
                           'webserver_newurl' : webserver_url}
            message = {'error' : False, 
                       'value' : json.dumps(server_info)}
            #print 'server: criado com sucesso!'
        except:
            #print 'server: falha na criação!'
            message = { 'error' : True,
                        'value' : u'Dados inválidos'}
        
        message = json.dumps(message)
        return HttpResponse(message,mimetype="text/javascript")        
    return HttpResponseBadRequest()

def get_webserver_pubkey():
    from Crypto.PublicKey import RSA
    try:
        webserver = WebServer.objects.get(name='SERVIDOR GRUYERE')
    except WebServer.DoesNotExist:
        webserver = WebServer.objects.create(name='SERVIDOR GRUYERE',
                                             url='https://gruyere.lps.ufrj.br/~gustavo/tbackup_server/')
        private = RSA.generate(1024)
        public = private.publickey()
        webserver.pvtkey = private.exportKey()
        webserver.pubkey = public.exportKey()
        webserver.save()
    return [webserver.pubkey, webserver.url]

@csrf_exempt
def retrieve(request):
    print 'server: recebi request'
    if request.method == 'GET':
        print 'server: é um GET'
        from django.utils import simplejson as json
        list_dests = list(Destination.objects.values_list('name', flat=True))
        print 'server: lista de dests - %s' % str(list_dests)
        return HttpResponse(json.dumps(list_dests))
    return HttpResponseBadRequest()    
        

@csrf_exempt
def backup(request):
    if request.method == 'POST':
        #try:
        #    origin = Origin.objects.get(pubkey=request.POST['origin_pubkey'])
        #except Origin.DoesNotExist:
        #    return HttpResponseBadRequest()
        from django.utils import simplejson as json
        #from base64 import b64encode, b64decode
        print 'é um post'
        request_values = json.loads(request.POST['value'])
        #filename = request_values['filename']
        #print filename
        destination = request_values['destination']
        date = request_values['date']
        #print destination
        #decoded_data = b64decode(request.POST['value']['file'])
        sha1sum_client = request_values['sha1sum']
        #sha1sum_server = get_sha1sum(decoded_data)
        from Crypto.Hash import SHA
        sha1 = SHA.new()
        i=0
        print 'server:'
        for chunk in request.FILES['file'].chunks():
            print 'chunk %i' %i
            i+=1
            sha1.update(chunk)
            
        sha1sum_server = sha1.hexdigest()
        if sha1sum_client != sha1sum_server:
            message = error(SHA1SUM_MATCH_ERROR)
            return HttpResponse(message, mimetype="text/javascript")
        origin_name = request_values['origin_name']
        print origin_name
        message = send_to_destination(request.FILES['file'], origin_name, destination, date, sha1sum_client)
        return HttpResponse(json.dumps(message), mimetype="text/javascript")
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
    print file_content
    print type(file_content)
    print origin_name
    print destination
    print sha1sum
    dest = Destination.objects.get(name=destination) #sempre existirá
    print dest
    if dest.islocal:
        print 'é local'
        from os import path, makedirs
        directory = path.join(dest.address,origin_name)
        print directory
        if not path.exists(directory):
            print 'caminho não existe'
            makedirs(directory)
            print 'caminho criado'
        with open(path.join(directory,file_content.name), 'w') as f:
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
    

def error(code):
    if code == SHA1SUM_MATCH_ERROR:
        msg = u'Arquivo corrompido durante transferência'
    
    return { 'error' : {'message' : msg,}}
