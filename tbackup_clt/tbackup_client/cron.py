# -*- coding: utf-8 -*-

#from django_cron import cronScheduler, Job
#from django.core.management import call_command

#class CheckBackups(Job):
#    '''
#    Cron Job that checks if there are backups to be made
#    '''
#    #run every minute
#    run_every = 60
#    
#    def job(self):
#        #print 'tbackup_agent --check-backups'
#        call_command("tbackup_agent", check_backups=True)
#
#cronScheduler.register(CheckBackups)
#
#class CheckNotSent(Job):
#    '''
#    Cron Job that checks local backups not yet sent to remote server and send them
#    '''
#    
#    #run every hour
#    run_every = 3600
#    
#    def job(self):
#        #print 'tbackup_agent --check-not-sent'
#        call_command("tbackup_agent", check_not_sent=True)
#
#cronScheduler.register(CheckNotSent)

#class UpdateConfigFile(Job):
#    '''
#    Cron Job that updates the configuration file
#    '''
#    
#    #run every 6 hours
#    run_every = 21600
#    
#    def job(self):
#        call_command("tbackup_agent", update_config=True)
        
#class DeleteOldLocalBackups(Job):
#    '''
#    Cron Job that deletes old local backups (older than 14 days)
#    '''
#    
#    #run every day
#    run_every = 86400
#    
#    def job(self):
#        call_command("tbackup_agent", delete_old_backups=True)
#        


        
