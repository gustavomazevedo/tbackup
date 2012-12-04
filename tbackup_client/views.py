# -*- coding: utf-8 -*-


#from tbackup_client import forms

#SERVER_URL = "https://gruyere.lps.ufrj.br/~gustavo/tbackup/server/register/"
#SERVER_URL = "http://127.0.0.1:8080/server/register/"

def index(request):
    pass
    #from django.shortcuts import redirect
    #return redirect('/tbackup_client/log/')
    #from tbackup_client.models import Origin
    #try:
    #    Origin.objects.get(pk=1)
    #except Origin.DoesNotExist:
    #    from django.shortcuts import redirect
    #    return redirect('/client/register/')
    #return redirect('/client/config/')

#def register(request):
#    from tbackup_client.forms import RegisterForm
#    from tbackup_client.models import Origin, WebServer, Destination
#    from django.shortcuts import render, render_to_response
#    from django.http import HttpResponse
#    
#    if request.method == 'POST':
#        form = RegisterForm(request.POST)
#        if form.is_valid():
#            try:
#                o = Origin.objects.get(pk=1)
#                message = u'Esta máquina já foi configurada no servidor. Seu nome é "' + o.name + '"' 
#                return render_to_response('register_msg.djhtml', { 'message' : message, })
#            except Origin.DoesNotExist:
#                from tbackup_client import  crypt
#                from django.utils import simplejson as json
#                pvtkey, pubkey = crypt.generate_rsa_keys(1024)
#                value = {
#                         'origin_name': request.POST['origin_name'],
#                         'origin_pubkey': pubkey,
#                        }
#                request_message = {
#                                   'error' : False,
#                                   'encrypted': False,
#                                   'key': False,
#                                   'json' : True,
#                                   'value' : json.dumps(value),
#                                  }
#                print request_message
#                #retrieve server info from file
#                import requests
#                
#
#                response = requests.post(SERVER_URL, request_message, verify=False)
#                if response.status_code != 200:
#                    return HttpResponse(content=response.text, content_type=response.headers['content-type'])
#                
#                response_text = json.loads(response.text)
#                print response_text
#                if response_text['error']:
#                    response_message = response_text['value']
#                    return render_to_response('register_msg.djhtml', { 'message' : response_message, })
#                Origin.objects.create(
#                                    name=request.POST['origin_name'],
#                                    pvtkey=pvtkey,
#                                    pubkey=pubkey)
#                response_values = json.loads(response_text['value'])
#                WebServer.objects.create(
#                                    name=response_values['webserver_name'],
#                                    pubkey=response_values['webserver_pubkey']
#                                    )
#                
#                response = requests.get(SERVER_URL.replace('/register/','/retrieve/'), verify=False)
#                if response.status_code != 200:
#                    return HttpResponse(content=response.text, content_type=response.headers['content-type'])
#                if response.status_code == 200:
#                    for destination in json.loads(response.text):
#                        Destination.objects.get_or_create(name=destination)
#                message = (u'Máquina configurada no servidor com sucesso! ' +
#                          u'<a href="../config/">Configurar transferência</a>')
#                return render_to_response('register_msg.djhtml', { 'message' : message, })
#    else:
#        try:
#            o = Origin.objects.get(pk=1)
#            message = u'Esta máquina já foi configurada no servidor. Seu nome é "' + o.name + '"' 
#            return render_to_response('register_msg.djhtml', { 'message' : message, })
#        except Origin.DoesNotExist:
#            form = RegisterForm()
#            return render(request, 'basic_form.djhtml',
#                { 'form': form,
#                  'formTitle' :u'Registro no Servidor Web',
#                  'formDescription' : u'Digite um nome para cadastrar este sistema no servidor',
#                })

#def config(request):
#    from tbackup_client.models import Config
#    from tbackup_client.models import Destination
#    from tbackup_client.forms import ConfigForm
#    if request.method == 'POST':
#        form = ConfigForm(request.POST)
#        if form.is_valid():
#            d = Destination.objects.get(id=request.POST['destination'])
#            Config.objects.get_or_create(
#                destination=d,
#                interval=int(request.POST['interval_0']) * int(request.POST['interval_1']))
#        from django.shortcuts import redirect
#        return redirect('/')
#    else:
#        from django.shortcuts import render
#        form = ConfigForm()
#        return render(request, 'basic_form.djhtml',
#            { 'form': form,
#              'formTitle' :u'Agendamento de Cópia de Segurança',
#              'formDescription' : u'Cadastre o destino e a periodicidade da cópia',
#            })

def restore(request, obj_id):
    pass