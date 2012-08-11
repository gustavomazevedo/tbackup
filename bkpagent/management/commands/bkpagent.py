# -*- coding: utf-8 -*-

import time
import os.path
import sys
import subprocess
import gzip
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand, CommandError
from django.utils import simplejson as json

import bkpagent as bc
from bkpagent.models import Server, BackupHistory

from django.conf import settings

NO_CHANGES = 0
NO_BACKUP = 1

class Command(BaseCommand):
    help = 'Updates configuration file and sets up backup jobs'

    def handle(self):
        dumpdatetime = str(datetime.now()).replace(' ','_').replace(':','-')
        dumpdatetime = dumpdatetime[:dumpdatetime.rfind('.')]
        self.dumppath = '%sbkpagent/dumps/%s.%s.json' % 
               (projectdir,projectname,dumpdatetime)
        self.zippath = self.dumppath.replace('.json','db.gz')

        configfile = configure()

        if not (configfile in (NO_CHANGES,NO_BACKUP)):
            now = datetime.now()
            backup_configs = json.load(open(configfile))
            dumped = False

            for bconf in backup_configs:
                destino = bconf['nome_destino']
                periodicidade = int(bconf['periodicidade'])
                last_backup = BackupHistory.objects.latest().dump_date
                delta = now - last_backup
                
                if delta.days >= periodicidade:
                    dumped = dumpdata() if dumped == False
                    execute_backup(bconf)
                    b = BackupHistory.objects.create(dump_date=now)
                    b.destination = destino
                    b.successfull = transfer_backup(bconf)
                    b.save()



def dumpdata():
    manage = projectdir + 'manage.py'
    installed_apps = settings.INSTALLED_APPS
    apps = ' '.join([a if not a.endswith('bkpagent') or a.startswith('django') for a in installed_apps])
#    for a in installed_apps:
#        apps += ' ' + a if not a.endswith('bkpagent')
    
    cmd = 'python %s dumpdata %s > %s' %
          (manage,apps,self.dumppath)
    stdout, stderr = ba.process(cmd)
    print stderr
    print stdout
    if stderr:
        return False
    return True

def execute_backup(bconf):
    f_in  = open(self.dumppath, 'rb')
    f_out = gzip.open(self.zippath,'wb',9)
    f_out.writelines(f_in)
    f_out.close()
    f_in.close()
    f_in.delete()
    
    cmd = '/usr/bin/rsync ssh -p %s -avz %s %s:%s' %
          (bconf['port'],self.zippath,bconf['destino'],bconf['dir'])
    stdout, stderr = ba.process(cmd)
    print stderr
    print stdout
    #filenamesLog = stdout.split('\n')[1:-4]
    
    log = {'error' : stderr, 'output': stdout}
    #send log to server
    #send_to_server(log)

def configure():
    #try:
    transfered = get_config_file()
    #except Exception as e:
    #    raise e
        
    #configuration file hasn't changed
    if transfered is None:
        return NO_CHANGES
    if "deleting" in transfered:
        return NO_BACKUP
    
    return ba.CONFIG_PATH + transfered  

def get_config_file()
    try:
        server = Server.objects.get(pk=1)
    except Server.DoesNotExist:
        server = ba.setup_server()
    cmd = '/usr/bin/rsync -e "ssh -p %s -l %s" -avz --delete-excluded %s %s' %
          (server.port,server.user,server.configpath,ba.CONFIG_PATH)
    stdout, stderr = ba.process(cmd)
    print stderr
    print stdout
    if stderr:
        #raise Exception('Could not retrieve config file', stderr)
        return None
    transfered = stdout.split('\n')[1]
    return transfered


