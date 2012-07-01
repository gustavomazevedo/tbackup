# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from tbackup.machines.models import Machine
import os


def index(request):
    infoMap = {}
    infoMap['title'] = u'Origens'
    machineList = SourceMachine.objects.all().order_by('-data')
    if len(machineList) == 0:
        infoMap['tableTitle'] = u'Não há nenhuma origem registrada!'
    else:
        infoMap['tableTitle'] = u'Lista de Origens Adicionadas'
        fieldnamesList = filter(lambda x: x!= 'id',machineList[0]._meta.get_all_field_names())
        fieldsList = []
        for fn in fieldnamesList:
            fieldsList.append(machineList[0]._meta.get_field_by_name(fn)[0])
        infoList = []
        for b in machineList:
            infoList.append([b.getPrettyHTML(f.name) for f in fieldsList])
        infoMap['machineList'] = infoList
        infoMap['fieldsList'] = fieldsList
        
    return render_to_response('machines/index.html', infoMap)
