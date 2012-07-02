# -*- coding: utf-8 -*-

import time
import os.path

from django.core.management.base import BaseCommand, CommandError
from backup_client.models import Config, Server, Backup

from datetime import datetime, timedelta

PROJECT_PATH = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))) + '/'

NO_CHANGES = 0
RESET = 1

class Command(BaseCommand):
    help = 'Updates configuration file and sets up backup jobs'
    
    def handle(self):
        try:
            configure()
        except e:
            raise CommandError('Could not connect to server')

        
        dt = datetime.now()
        dt -= timedelta(seconds=dt.second, microseconds=dt.microsecond)

        backups = Backup.objects.all()
        for b in backups:
            delta = dt - b.datetime
            if not to_minutes(delta)%b.minutes_delta:
                execute_backup(b)


def to_minutes(td):
    """
    Converts timedelta objects to minutes
    """
    return td.seconds // 60 + td.days * 24 * 60

def execute_backup(backup):
    manage = PROJECT_PATH + 'manage.py'
    jsonfile = 
    cmd = 'usr/bin/python %s dumpdata > '
    cmd = '/usr/bin/rsync ssh -p %s -avz %s %s' %
          (backup.destination_port,bkpfile_path,backup.destination_dir)
    stdout, stderr = process(cmd)

def configure():
    try:
        transfered = get_config_file()
    except Exception as e:
        raise e
        
    #configuration file hasn't changed
    if not transfered:
        return NO_CHANGES
    if "deleting" in transfered:
        Backup.objects.all().delete()
        return RESET
    
    parsed = json.load(open(CONFIG_FILE))
    
    #config = Config.objects.get(pk=1)
    #try:
    #    config.file = open(CONFIG_PATH, "r")
    #    config.ctime = time.ctime(os.path.getctime(CONFIG_PATH))
    #    config.save()
    #
    #return config.file

def get_config_file()
    server = Server.objects.get(pk=1)
    cmd = '/usr/bin/rsync ssh -p %s -avz --delete-excluded %s %s' %
          (server.port,server.config_path,CONFIG_PATH)
    stdout, stderr = process(cmd)
    if stderr:
        raise Exception('Could not retrieve config file', stderr)
    transfered = stdout.split('\n')[1]
    return transfered

def process(cmd)
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE,
                                        shell=True)
    return p.communicate()