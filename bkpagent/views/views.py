# -*- coding: utf-8 -*-
from os.path import expanduser
import subprocess
import requests

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, render_to_response, redirect
from django.utils import simplejson as json
from bkpagent.forms.Client import ClientForm
from bkpagent.models import BackupHistory, Client

HOMEPATH = expanduser("~")

SERVER_URL = "https://gruyere.lps.ufrj.br/~gustavo/tbackup/bkpserver/register/"
#SERVER_URL = "http://127.0.0.2:8000/bkpserver/register/"


def index(request):
    try:
        Client.objects.get(pk=1)
    except Client.DoesNotExist:
        return redirect('/register/')

    if request.method == 'POST':
        form = TransferForm(request.POST)
        if form.is_valid():
            pass
    else:
        form = TransferForm()
        return render(request, 'base_site.html', { 'form' : form, })

@login_required
def register_to_server(request):
    if request.method == 'POST':
        try:
            c = Client.objects.get(pk=1)
            message = u'Esta máquina já foi configurada no servidor. Seu nome é "' + c.name + '"' 
            return render_to_response('register_msg.html', { 'message' : message, })
        except Client.DoesNotExist:
            form = ClientForm(request.POST)
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

                Client.objects.create(name=request.POST['name'])

                message = u'Máquina configurada no servidor com sucesso!'
                return render_to_response('register_msg.html', { 'message' : message, })
    else:
        form = ClientForm()
        return render(request, 'base_site.html', { 'form': form, })

def _check_ssh_keys():
    try:
        f = open(HOMEPATH + "/.ssh/id_rsa.pub", "r")
    except IOError:
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
    
@login_required
def log(request):
    infoMap = {}
    infoMap['title'] = u'Histórico'
    logList = BackupHistory.objects.all().order_by('-dump_date')
    if len(logList) == 0:
        infoMap['tableTitle'] = u'Não há nenhum log registrado!'
    else:
        infoMap['tableTitle'] = u'Lista de Logs Realizados'
        fieldnamesList = filter(lambda x: x!= 'id',logList[0]._meta.get_all_field_names())
        fieldsList = []
        for fn in fieldnamesList:
            fieldsList.append(logList[0]._meta.get_field_by_name(fn)[0])
        infoList = []
        for b in logList:
            infoList.append([b.getFormatted(f.name) for f in fieldsList])
        infoMap['logList'] = infoList
        infoMap['fieldsList'] = fieldsList
        
    return render_to_response('logs/index.html', infoMap)

#@login_required
#def restore(request, filename):
#    if request.method == 'GET':
