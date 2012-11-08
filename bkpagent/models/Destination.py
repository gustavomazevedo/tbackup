# -*- coding: utf-8 -*-

'''
Created on 28/10/2012

@author: gustavo
'''

from django.db import models

class Destination(models.Model):
    '''
    name = nome específico do destino. Padrão preferível: "Projeto - Máquina"
        (ex.: "Sapem - Gruyere")
    full_address = endereço completo de destino (<user>@<address>:<dir>)
    port = porta aberta para acesso SSH
    '''
    
    class Meta:
        '''
        metadatadocs
        '''
        app_label = 'bkpagent'
        verbose_name = 'servidor'
        verbose_name_plural = 'servidores'
        ordering = ['name']
    
    name = models.CharField(max_length=80, verbose_name='nome')
    full_address = models.CharField(max_length=512, verbose_name=u'endereço')
    port = models.CharField(max_length=5, verbose_name='porta')
        
    def __unicode__(self):
        '''
        returnstringdocs
        '''
        return self.name