# -*- coding: utf-8 -*-
from os.path import expanduser
import subprocess
import requests

from django.http import HttpResponse
from django.shortcuts import render, render_to_response
from django.utils import simplejson as json
from bkpagent.forms import ThisMachineForm
from bkpagent.models import BackupHistory, Server, ThisMachine

HOMEPATH = expanduser("~")

SERVER_URL = "https://gruyere.lps.ufrj.br/~gustavo/tbackup/bkpserver/register/"
#SERVER_URL = "http://127.0.0.2:8000/bkpserver/register/"

def register_to_server(request):
    if request.method == 'POST':
        try:
            tm = ThisMachine.objects.get(pk=1)
            message = u'Esta máquina já foi configurada no servidor. Seu nome é "' + tm.name + '"' 
            return render_to_response('register_msg.html', { 'message' : message, })
        except ThisMachine.DoesNotExist:
            form = ThisMachineForm(request.POST)
            if form.is_valid():
                pubkey = _check_ssh_keys()
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

                thismachine = ThisMachine.objects.create(name=request.POST['name'])

                message = u'Máquina configurada no servidor com sucesso!'
                return render_to_response('register_msg.html', { 'message' : message, })
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
