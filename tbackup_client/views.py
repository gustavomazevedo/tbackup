# -*- coding: utf-8 -*-


#from tbackup_client import forms

SERVER_URL = "https://gruyere.lps.ufrj.br/~gustavo/tbackup/server/register/"

def index(request):
    from tbackup_client.models import Origin
    try:
        Origin.objects.get(pk=1)
    except Origin.DoesNotExist:
        from django.shortcuts import redirect
        return redirect('/client/register/')
    return redirect('/client/config/')

def register(request):
    from tbackup_client.forms import RegisterForm
    from tbackup_client.models import Origin, WebServer
    from django.shortcuts import render, render_to_response
    from django.http import HttpResponse
    
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            try:
                o = Origin.objects.get(pk=1)
                message = u'Esta máquina já foi configurada no servidor. Seu nome é "' + o.name + '"' 
                return render_to_response('register_msg.html', { 'message' : message, })
            except Origin.DoesNotExist:
                from Crypto.PublicKey import RSA
                from Crypto import Random
                import requests
                from django.utils import simplejson as json
                private = RSA.generate(1024, Random.new().read)
                public = private.publickey()
                pvtkey=private.exportKey()
                
                pubkey=public.exportKey()
    
                values = {
                    'origin_name': request.POST['name'],
                    'origin_sshkey': pubkey,
                }
                url = SERVER_URL
                
                response = requests.post(url, values, verify=False)
                if response.status_code != 200:
                    return HttpResponse(content=response.text, content_type=response.headers['content-type'])
                if 'error' in response.text:
                    message = json.loads(response.text)['error']['message']
                    return render_to_response('register_msg.html', { 'message' : message, })
                Origin.objects.create(
                                    name=request.POST['name'],
                                    pvtkey=pvtkey,
                                    pubkey=pubkey)
                message = u'Máquina configurada no servidor com sucesso!'
                return render_to_response('register_msg.html', { 'message' : message, })
    else:
        try:
            o = Origin.objects.get(pk=1)
            message = u'Esta máquina já foi configurada no servidor. Seu nome é "' + o.name + '"' 
            return render_to_response('register_msg.html', { 'message' : message, })
        except Origin.DoesNotExist:
            form = RegisterForm()
            return render(request, 'basic_form.djhtml',
                { 'form': form,
                  'formTitle' :u'Registro no Servidor Web',
                  'formDescription' : u'Digite um nome para cadastrar este sistema no servidor',
                })


def log(request):
    pass


def config(request):
    from tbackup_client.forms import ConfigForm
    if request.method == 'POST':
        pass
    else:
        from django.shortcuts import render
        form = ConfigForm()
        return render(request, 'basic_form.djhtml',
            { 'form': form,
              'formTitle' :u'Agendamento de Cópia de Segurança',
              'formDescription' : u'Cadastre o destino e a periodicidade da cópia',
            })