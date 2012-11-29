# -*- coding: utf-8 -*-

from datetime import datetime

from django.db import models

# Create your models here.

class Destination(models.Model):
    name = models.CharField(max_length=80, verbose_name='nome')
    
    class Meta:
        verbose_name = 'destino'
        ordering = ['name']
        
    def __unicode__(self):
        return self.name

class Origin(models.Model):
    name = models.CharField(max_length=80, verbose_name='nome')
    pvtkey = models.TextField(verbose_name=u'chave privada')
    pubkey = models.TextField(verbose_name=u'chave pública')
    
    class Meta:
        verbose_name = 'origem'
        verbose_name_plural = 'origem'
        ordering = ['name']
    
    def __unicode__(self):
        return self.name

class WebServer(models.Model):
    name = models.CharField(max_length=80, verbose_name='nome')
    pubkey = models.TextField(verbose_name = u'chave pública')
    url = models.CharField(max_length=1024)
    
    def __unicode__(self):
        return self.name

class Config(models.Model):
    destination = models.ForeignKey('Destination')
    interval = models.IntegerField(verbose_name='periodicidade')
    last_backup = models.DateTimeField(default=datetime.now(),verbose_name=u'data do último backup')

class BackupStatus(models.Model):
    executing = models.BooleanField(default=False)
    
class Log(models.Model):
    #origin = models.ForeignKey('Origin')
    destination = models.ForeignKey('Destination')
    date = models.DateTimeField(verbose_name='data')
    filename = models.CharField(max_length=1024, verbose_name='arquivo')
    local_status = models.BooleanField() 
    remote_status = models.BooleanField()
    
        
