# -*- coding: utf-8 -*-
from os.path import expanduser
import subprocess
import requests

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from django.utils import simplejson as json
from bkpagent.forms import ThisMachineForm
from bkpagent.models import BackupHistory, Server, ThisMachine

HOMEPATH = expanduser("~")

#@csrf_exempt
def register_to_server(request):
    if request.method == 'POST':
        try:
            tm = ThisMachine.objects.get(pk=1)
            error_message = u'Esta máquina já foi configurada no servidor. Seu nome é "' + tm.name + '"' 
            return render_to_response('register_msg.html', { 'message' : error_message, })
        except ThisMachine.DoesNotExist:
            form = ThisMachineForm(request.POST)
            if form.is_valid():
                pubkey = _check_ssh_keys()
                values = {
                    'origin_name': request.POST['name'],
                    'origin_sshkey': pubkey,
                }
                #url = "http://gruyere.lps.ufrj.br/~tbackup/bkpserver/register/"
                url = "http://127.0.0.2:8000/bkpserver/register/"
                response = requests.post(url,values)
                if response.status_code != 200:
                    return HttpResponse(content=response.text, content_type=response.headers['content-type'])
                if 'error' in response.text:
                    error_message = json.loads(response.text)['error']['message']
                    return render_to_response('register_msg.html', { 'message' : error_message, })
                    
                thismachine = ThisMachine.objects.create(name=request.POST['name'])
                
                success_message = u'Máquina configurada no servidor com sucesso!'
                return render_to_response('register_msg.html', { 'message' : success_message, })
    else:
        form = ThisMachineForm()
        return render(request, 'base_site.html', { 'form': form, })
        
        

def _check_ssh_keys():
    try:
        f = open(HOMEPATH + "/.ssh/id_rsa.pub", "r")
    except IOError as e:
        _run("ssh-keygen -q -N '' -f " + HOMEPATH + "/.ssh/id_rsa")
        f = open(HOMEPATH + "/.ssh/id_rsa.pub", "r")
        
    pubkey = f.read()
    if pubkey[-1] == "\n":
        pubkey = pubkey[:-1]
    f.close()
    return pubkey             
                
def _run(cmd):
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE,
                                        shell=True)
    return p.communicate()        
