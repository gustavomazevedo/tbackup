# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from tbackup.logs.models import LogHistory, ArquivoBackup
import os


def index(request):
    infoMap = {}
    infoMap['title'] = u'Histórico'
    logList = LogHistory.objects.all().order_by('-data')
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
            infoList.append([b.getPrettyHTML(f.name) for f in fieldsList])
        infoMap['logList'] = infoList
        infoMap['fieldsList'] = fieldsList
        
    return render_to_response('logs/index.html', infoMap)
