# -*- coding: utf-8 -*-

'''
Created on 28/10/2012

@author: gustavo
'''

from django.db import models

class BackupHistory(models.Model):
    '''
    classdocs
    '''

    class Meta:
        '''
        metadatadocs
        '''
        app_label = 'bkpagent'
        verbose_name = u'histórico'
    
    dump_date = models.DateTimeField(verbose_name='data')
    filename = models.CharField(verbose_name='arquivo', max_length=1024)
    destination = models.ForeignKey('Destination', verbose_name='destino')
    local_copy = models.BooleanField(verbose_name='backup local')
    remote_copy = models.BooleanField(verbose_name='backup remoto')
    
        
    def __unicode__(self):
        '''
        
        '''
        return str(self.dump_date)

    def getFormatted(self, fieldName):
        '''
        
        '''
        val = getattr(self, fieldName)
        if fieldName == 'filename':
            return val.split('/')[-1];
        elif fieldName == 'dump_date':
            return u'%02d/%02d/%04d às %02d:%02d' % (val.day, val.month, val.year, val.hour, val.minute)
        elif fieldName == 'destination':
            return val.name;
        elif fieldName in ('local_ok','remote_ok'):    
            if val: return 'OK'
            else: return 'ERRO'
        return val
        