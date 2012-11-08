# -*- coding: utf-8 -*-

import os
import sys
import subprocess
import gzip
#from cStringIO import StringIO
from datetime import datetime

from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand, make_option
from django.db.models import Max
from django.utils import simplejson as json

import bkpagent
from bkpagent.models import Client, Server, BackupHistory, Destination


PROJECT_DIR = os.path.normpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../../../'))
PROJECT_NAME = PROJECT_DIR.split('/')[-2]

CONFIG_DIR = os.path.normpath(os.path.join(PROJECT_DIR, 'bkpagent/configs/'))
DUMP_DIR = os.path.normpath(os.path.join(PROJECT_DIR, 'bkpagent/dumps/'))

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--execute_backup', '-e',
            dest='execute_backup',
            default=False,
            help='Sets up backup jobs'),
        make_option('--update-config', '-u',
            dest='update_config',
            default=False,
            help='Updates configuration file'),
        make_option('--delete-old-backups', '-d',
            dest='delete_old_backups',
            default=False,
            help='Deletes local backups older than 14 days'),
        make_option('--check-not-sent', '-c',
            dest='check_not_sent',
            default=False,
            help='Sends pending local backups to remote server')
        )
    
    def handle(self, *args, **options):
        #Don't accept commands if client is not registered
        try:
            Client.objects.get(pk=1)
        except Client.DoesNotExist:
            return
        
        backupHandler = BackupHandler()
        if options['execute_backup']:
            backupHandler.execute_backup()
        elif options['update_config']:
            backupHandler.update_config()
        elif options['delete_old_backups']:
            backupHandler.delete_old_backups()
        elif options['check_not_sent']:
            backupHandler.check_not_sent()
        

class BackupHandler():

    def delete_old_backups(self):
        fourteen_days_ago = datetime.now() - datetime.timedelta(days=14)
        backuphistory = BackupHistory.objects.filter(
            local_copy=True,
            remote_copy=True,
            dump_date__lt=fourteen_days_ago)
        
        for backup in backuphistory:
            os.remove(os.path.join(DUMP_DIR, backup.filename))
            backup.local_copy = False
            backup.save()

    def update_config(self):
        try:
            server = Server.objects.get(pk=1)
        except Server.DoesNotExist:
            server = bkpagent.setup_server()
            
        cmd = ('rsync -e "ssh -p {0} -l {1}" -avz --delete-excluded {2} {3}'
               .format(server.port, server.user, server.configpath, CONFIG_DIR))
            
        stdout, stderr = self.process(cmd)
        self.command_log(stdout, stderr)
    
    def check_not_sent(self):
        not_sent = BackupHistory.objects.filter(
            local_copy=True,
            remote_copy=False)
        for backup in not_sent:
            self.remote_backup(backup)
            backup.save()
        
    def execute_backup(self):
        
        now = datetime.now()
        #self.dump_path, self.zip_path = self.get_dump_path(now)
        
        config_file = self.get_config_file()

        if config_file is not None:
            backup_configs = json.load(config_file)
            #dumped = False

            for conf in backup_configs:
                periodicidade = int(conf['periodicidade'])
                key, last_backup = (BackupHistory.objects.get(
                    destination__name=conf['nome_destino'])
                    .aggregate(Max('dump_date')))
                delta = now - last_backup
                
                if delta.days >= periodicidade:
                    destination = Destination.objects.get(name=conf['nome_destino'])
                    b = (BackupHistory.objects.create(
                        destination=destination,
                        dump_date=now))
                    self.local_backup(b)
                    b.save()
                    self.remote_backup(b)
                    b.save()
    
    def local_backup(self, backup):
        dt = str(backup.dump_date).replace(' ','_').replace(':','-')
        self.date = dt[:dt.rfind('.')]
        
        client = Client.objects.get(pk=1)
        filename = client.slug + self.date
        
        installed_apps = settings.INSTALLED_APPS
        apps = [a for a in installed_apps if not a.startswith('django')]
               
        #content = StringIO()
        #call_command('dumpdata', *apps, stdout=content)
        call_command('dumpdata', *apps, stdout=open(os.path.join(DUMP_DIR,filename),"w"))
        #content.seek(0)
        
        newfilename = filename + 'tar.gz'
        
        f_in  = open(filename, 'rb')
        f_out = gzip.open(newfilename,'wb',9)
        
        f_out.writelines(f_in)
        f_out.close()
        f_in.close()
        f_in.delete()
        os.remove(filename)   
        
        backup.filename = newfilename
        backup.local_copy = True

    
    def remote_backup(self, backup):
        
        cmd = ('rsync ssh -p {0} -avz {1} {2}'
               .format(
                   backup.destination.port,
                   backup.filename,
                   backup.destination.full_address)
               )
        stdout, stderr = self._run(cmd)
        
        if stderr:
            return
        
        backup.remote_copy = True    
    
    def get_config_file(self):
        try:
            client = Client.objects.get(pk=1)
            return open(os.path.join(CONFIG_DIR,client.slug), "r")
        except:
            return None
    
    def _run(self, cmd):
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                                            stderr=subprocess.PIPE,
                                            shell=True)
        return p.communicate()
    
    #def command_log(self, stdout, stderr):
    #    with open(os.path.join(CONFIG_DIR,"stdout.txt"),"a") as f:
    #        f.write(stdout + "\n")
    #    with open(os.path.join(CONFIG_DIR,"stderr.txt"),"a") as f:
    #        f.write(stderr + "\n")

    #def transfer_backup(self, d):
    #    self.copy_tree(d)
    # 
    #    cmd = 'rsync ssh -p {0} -avz {1} {2}'.format(d.port,self.zip_path,d.full_address)
    #    
    #    stdout, stderr = self.process(cmd)
    #    
    #    self.command_log(stdout, stderr)
    #    #filenamesLog = stdout.split('\n')[1:-4]
    #    
    #    log = {'error' : stderr, 'output': stdout}
    #    #send log to server
    #    self.send_log_to_web_server(log)
                
    #def copy_tree(self, d):
    #    cmd = 'rsync ssh -p {0} -a -f"+ */" -f"- *" {1} {2}'.format(d.port,os.path.dirname(os.path.dirname(self.zip_path)),d.full_address)
    
    #def oldest_file_in_tree(self, rootfolder, extension=".db.gz"):
    #    return min(
    #        (os.path.join(dirname, filename)
    #        for dirname, dirnames, filenames in os.walk(rootfolder)
    #        for filename in filenames
    #        if filename.endswith(extension)),
    #        key=lambda fn: os.stat(fn).st_mtime)