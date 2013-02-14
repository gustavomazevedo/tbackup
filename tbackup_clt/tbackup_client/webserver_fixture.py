# -*- coding: utf-8 -*-


def run():
    from tbackup_client.models import WebServer
    #print 'gravando webserverInfo'
    ws = WebServer.objects.create(name='Gruyere WebServer',
                                  #url='https://gruyere.lps.ufrj.br/~gustavo/tbackup_server/')
                                  url='http://127.0.0.1:8080/')
    #print ws.name
    #print ws.url
    ws.save()
