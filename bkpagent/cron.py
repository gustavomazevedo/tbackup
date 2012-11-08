# -*- coding: utf-8 -*-

from django_cron import Job
from django.core.management import call_command

class CheckBackups(Job):
    '''
    Cron Job that checks if there are backups to be made
    '''
    #run every 5 minutes (300 seconds)
    run_every = 300

    def job(self):
        call_command("bkpagent", execute_backup=True)

class CheckNotSent(Job):
    '''
    Cron Job that checks local backups not yet sent to remote server and send them
    '''
    
    #run every hour
    run_every = 3600
    
    def job(self):
        call_command("bkpagent", check_not_sent=True)
  
class UpdateConfigFile(Job):
    '''
    Cron Job that updates the configuration file
    '''
    
    #run every 6 hours
    run_every = 21600
    
    def job(self):
        call_command("bkpagent", update_config=True)
        
class DeleteOldLocalBackups(Job):
    '''
    Cron Job that deletes old local backups (older than 14 days)
    '''
    
    #run every day
    run_every = 86400
    
    def job(self):
        call_command("bkpagent", delete_old_backups=True)
        


        
