# -*- coding: utf-8 -*-

from django.db import models

class Destination(models.Model):
    name = models.CharField(max_length=80, verbose_name='nome')
    islocal = models.BooleanField(verbose_name='local')
    address = models.CharField(max_length=1024, verbose_name=u'endereço')    
    port = models.CharField(max_length=5, blank=True, verbose_name='porta')

    class Meta:
        verbose_name = 'destino'
        ordering = ['name']
    
    def __unicode__(self):
        return self.name

class Origin(models.Model):
    name = models.CharField(max_length=80, verbose_name='nome')
    pubkey = models.TextField(verbose_name=u'chave pública')
    
    class Meta:
        verbose_name = 'origem'
        verbose_name_plural = 'origens'
        ordering = ['name']
    
    def __unicode__(self):
        return self.name

class WebServer(models.Model):
    name = models.CharField(max_length=80, verbose_name='nome')
    url = models.CharField(max_length=1024)
    pvtkey = models.TextField(verbose_name = 'chave privada')
    pubkey = models.TextField(verbose_name = u'chave pública')

class ConfigHistory(models.Model):
    pass

class Log(models.Model):
    origin = models.ForeignKey('Origin')
    destination = models.CharField(max_length=80, verbose_name='destino')
    date = models.DateTimeField(verbose_name='data')
    filename = models.CharField(max_length=1024, verbose_name='arquivo')  
    status = models.BooleanField()

