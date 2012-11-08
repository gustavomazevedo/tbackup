# -*- coding: utf-8 -*-

'''
Created on 28/10/2012

@author: gustavo
'''

from django.db import models
from django.template.defaultfilters import slugify

class Client(models.Model):
    '''
    modeldocs
    '''
    
    class Meta:
        '''
        metadatadocs
        '''
        app_label = 'bkpagent'
    
    name = models.CharField(max_length=80)
    slug = models.SlugField(max_length=80)
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Client, self).save(*args, **kwargs)
        
    def __unicode__(self):
        '''
        returnstringdocs
        '''
        return self.name