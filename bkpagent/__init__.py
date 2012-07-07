# -*- coding: utf-8 -*-

from os import path

CONFIG_PATH = path.abspath(__file__) + '/config/'


def to_minutes(td):
    """
    Converts timedelta objects to minutes
    """
    return td.seconds // 60 + td.days * 24 * 60

def process(cmd)
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE,
                                        shell=True)
    return p.communicate()
    
def setup_server()
    server = Server.objects.create(name='Gruyere')
    server.user = 'gustavo'
    server.configpath = 'gruyere.lps.ufrj.br:~/tb/tbackup/bkpserver/config/%s/' % getattr(settings,MACHINE_ADDRESS)
    server.port = '22'
    server.save()
    return server
