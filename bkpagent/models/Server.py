# -*- coding: utf-8 -*-

'''
Created on 28/10/2012

@author: gustavo
'''

from django.db import models

class Server(models.Model):
    '''
    modeldocs
    '''
    
    class Meta:
        '''
        metadatadocs
        '''
        app_label = 'bkpagent'
    
    
    name = models.CharField(max_length=80)
    configpath = models.CharField(max_length=1024)
    port = models.CharField(max_length=5)
        
    def __unicode__(self):
        '''
        returnstringdocs
        '''
        return self.name