# -*- coding: utf-8 -*-

import requests

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseBadRequest
#from django.shortcuts import render, render_to_response
from django.utils import simplejson as json
#from bkpagent.forms import ThisMachineForm
#from bkpagent.models import BackupHistory, Server, ThisMachine

#HOMEPATH = expanduser("~")

#SERVER_URL = "https://gruyere.lps.ufrj.br/~gustavo/tbackup/bkpserver/register/"
#SERVER_URL = "http://127.0.0.2:8000/bkpserver/register/"

@login_required
def recover(request):
    if request.method == "POST":
        c = Client.objects.get(name=request.POST["name"])
        if c is None:
            return HttpResponseBadRequest()
        if not verifyRequest(request.POST["pgp_sign"], c.public_key):
            return HttpResponseBadRequest()
        
    return HttpResponseBadRequest()