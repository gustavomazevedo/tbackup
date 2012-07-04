# -*- coding: utf-8 -*-

import time
import os.path
import sys
import subprocess
import gzip
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand, CommandError
from bkpclient.models import Server
import bkpclient as bc

projectdir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))) + '/'
sys.path.insert(0,projectdir)
import settings
projectname = projectdir.split('/')[-2]

NO_CHANGES = 0
RESET = 1


class Command(BaseCommand):
    help = 'Updates configuration file and sets up backup jobs'
    
    def handle(self):
        dumpdatetime = str(datetime.now()).replace(' ','_').replace(':','-')
        dumpdatetime = dumpdatetime[:dumpdatetime.rfind('.')]
        self.dumppath = '%sbkpclient/dumps/%s.%s.json' % 
               (projectdir,projectname,dumpdatetime)
        self.zippath = self.dumppath.replace('.json','db.gz')
        
        try:
            configfile = configure()
        except e:
            raise CommandError('Could not connect to server')

        if not (configpath in (NO_CHANGES,RESET)):
            dt = datetime.now()
            dt -= timedelta(seconds=dt.second, microseconds=dt.microsecond)
            backup_configs = json.load(open(configfile))
            
            dumped = False
            for bconf in backup_configs:
                primeirobkp = datetime.strptime(bconf['primeirobkp'],'%d/%m/%y %H:%M')
                periodicidade = int(bconf['periodicidade'])
                delta = dt - primeirobkp
                if bc.to_minutes(delta) % periodicidade == 0:
                    dumped = dumpdata() if dumped == False
                    execute_backup(bconf)

def dumpdata():
    manage = projectdir + 'manage.py'
    installed_apps = getattr(settings,'INSTALLED_APPS')
    apps = ' '.join([a if not a.endswith('bkpclient') for a in installed_apps])
#    for a in installed_apps:
#        apps += ' ' + a if not a.endswith('bkpclient')
    
    cmd = '/usr/bin/python %s dumpdata %s > %s' %
          (manage,apps,self.dumppath)
    stdout, stderr = bc.process(cmd)
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
          (bconf['port'],self.zippath,bconf['destination'],bconf['dir'])
    stdout, stderr = bc.process(cmd)
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
        #Backup.objects.all().delete()
        return RESET
    
    return bc.CONFIG_PATH + transfered  

def get_config_file()
    try:
        server = Server.objects.get(pk=1)
    except Server.DoesNotExist:
        server = bc.setup_server()
    cmd = '/usr/bin/rsync -e "ssh -p %s -l %s" -avz --delete-excluded %s %s' %
          (server.port,server.user,server.configpath,bc.CONFIG_PATH)
    stdout, stderr = bc.process(cmd)
    print stderr
    print stdout
    if stderr:
        #raise Exception('Could not retrieve config file', stderr)
        return None
    transfered = stdout.split('\n')[1]
    return transfered


