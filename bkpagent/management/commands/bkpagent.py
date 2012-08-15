# -*- coding: utf-8 -*-

import time
import os
import sys
import subprocess
import gzip
from datetime import datetime
from django.core.management.base import BaseCommand, CommandError
from django.utils import simplejson as json

from bkpagent.models import Server, BackupHistory, Destination

from django.conf import settings

PROJECT_DIR = os.path.normpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../../../'))
PROJECT_NAME = PROJECT_DIR.split('/')[-2]

CONFIG_DIR = os.path.normpath(os.path.join(PROJECT_DIR, 'bkpagent/configs/'))
DUMP_DIR = os.path.normpath(os.path.join(PROJECT_DIR, 'bkpagent/dumps/'))

NO_CHANGES = 0
NO_BACKUP = 1

class Command(BaseCommand):
    help = 'Updates configuration file and sets up backup jobs'

    def handle(self):
        bkpHandler = BackupHandler()
        
        

class BackupHandler():

    def __init__(self):
        self.update_backup_history()
        
        self.dump_path, self.zip_path = self.get_dump_path()
        
        config_file = self.configure()

        if not (config_file in (NO_CHANGES,NO_BACKUP)):
            now = datetime.now()
            backup_configs = json.load(open(config_file))
            #dumped = False

            for conf in backup_configs:
                periodicidade = int(conf['periodicidade'])
                last_backup = BackupHistory.objects.latest().dump_date
                delta = now - last_backup
                
                if delta.days >= periodicidade:
                    b = BackupHistory.objects.create(dump_date=now)
                    dump_ok = self.dumpdata() #if dumped == False
                    if dump_ok:
                        backup_ok = self.execute_backup(conf)
                        if backup_ok:
                            b.local_ok = True
                            b.destination = Destination.objects.get_or_create(name=conf['nome_destino'])
                            b.destination.full_address = conf['destino'] + ':' + conf['dir']
                            b.destination.port = conf['port'] 
                            b.destination.save()
                            
                    b.save()
        
        self.send_backups()
                    
    def update_backup_history(self):
        backuphistory = BackupHistory.objects.filter(local_ok=True)
        for b in backuphistory:
            try:
                f = open(os.path.join(CONFIG_DIR, b.filename),"r")
                f.close()
            except:
                b.local_ok = False
                b.save()
        
    def send_backups(self):        
        backuphistory = BackupHistory.objects.filter(remote_ok=False)
        for b in backuphistory:
            b.remote_ok = transfer_backup(b)
    
    def get_dump_path(self):
        dump_dt = str(datetime.now()).replace(' ','_').replace(':','-')
        dump_dt = dump_dt[:dump_dt.rfind('.')]
        
        _dump = '{0}{1}/{2}.json'.format(CONFIG_DIR, PROJECT_NAME, dump_dt)
        _zip = _dump.replace('.json','db.gz')
        
        return [_dump, _zip]
    
    def dumpdata(self):
        manage = projectdir + 'manage.py'
        installed_apps = settings.INSTALLED_APPS
        apps = ' '.join([a if not a.endswith('bkpagent') or a.startswith('django') for a in installed_apps])
        cmd = 'python {0} dumpdata {1} > {2}'.format(manage, apps, self.dump_path)
        stdout, stderr = self.process(cmd)
        self.command_log(stdout,stderr)
        
        if stderr:
            return False
        return True

    def command_log(self, stdout, stderr):
        with open(os.path.join(CONFIG_DIR,"stdout.txt","a") as f:
            f.write(stdout + "\n")
        with open(os.path.join(CONFIG_DIR,"stderr.txt","a") as f:
            f.write(stderr + "\n")
        
    def execute_backup(self, conf):
        f_in  = open(self.dump_path, 'rb')
        f_out = gzip.open(self.zip_path,'wb',9)
        
        try:
            f_out.writelines(f_in)
            f_out.close()
        except:
            #espaço esgotado, deleta arquivos antigos até que haja espaço suficiente
            zipped = False
            while zipped == False:
                f = self.oldest_file_in_tree(DUMP_DIR)
                os.remove(f)
                try:
                    f_out.writelines(f_in)
                    f_out.close()
                    zipped = True
                    
        f_in.close()
        f_in.delete()    
        
    def oldest_file_in_tree(rootfolder, extension=".db.gz"):
        return min(
            (os.path.join(dirname, filename)
            for dirname, dirnames, filenames in os.walk(rootfolder)
            for filename in filenames
            if filename.endswith(extension)),
            key=lambda fn: os.stat(fn).st_mtime)

        
    def transfer_backup(self, d):
        self.copy_tree(d)
    
        cmd = 'rsync ssh -p {0} -avz {1} {2}'.format(d.port,self.zip_path,d.full_address)
        
        stdout, stderr = self.process(cmd)
        
        self.command_log(stdout, stderr)
        #filenamesLog = stdout.split('\n')[1:-4]
        
        log = {'error' : stderr, 'output': stdout}
        #send log to server
        send_to_server(log)

    def copy_tree(self, d):
        cmd = 'rsync ssh -p {0} -a -f"+ */" -f"- *" {1} {2}'.format(d.port,os.path.dirname(os.path.dirname(self.zip_path)),d.full_address)
    
    def configure(self):

        transfered = get_config_file()
            
        #configuration file hasn't changed
        if transfered is None:
            return NO_CHANGES
        if "deleting" in transfered:
            return NO_BACKUP
        
        return os.path.join(CONFIG_DIR,transfered)

    def get_config_file(self)
        try:
            server = Server.objects.get(pk=1)
        except Server.DoesNotExist:
            server = setup_server()
            
        cmd = 'rsync -e "ssh -p {0} -l {1}" -avz --delete-excluded {2} {3}'
            .format(server.port, server.user, server.configpath, CONFIG_DIR)
            
        stdout, stderr = self.process(cmd)
        self.command_log(stdout, stderr)
        
        if stderr:
            return None
        return stdout.split('\n')[1]


