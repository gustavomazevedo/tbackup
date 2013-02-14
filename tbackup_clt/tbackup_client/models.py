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
    
    def __unicode__(self):
        from forms import TIMEDELTA_CHOICES
        i = ''
        n = ''
        for div, name in reversed(TIMEDELTA_CHOICES):
            if self.interval % div == 0:
                i = str(self.interval / div)
                n = name if i != '1' else name[0:-1]
                break
        return self.destination.name + " a cada " + i + " " + n  

class BackupStatus(models.Model):
    executing = models.BooleanField(default=False)
    
class Log(models.Model):
    #origin = models.ForeignKey('Origin')
    destination = models.ForeignKey('Destination')
    date = models.DateTimeField(verbose_name='data')
    filename = models.CharField(max_length=1024, verbose_name='arquivo')
    local_status = models.BooleanField() 
    remote_status = models.BooleanField()
    
    def __unicode__(self):
        return self.filename
    
    def restore_link(self):
        if self.remote_status:
            return '<a href="/tbackup_client/restore/%s">Restore<img src="/static/img/Refresh.png"/></a>' % self.id
        return ''
    restore_link.short_description = 'Restaurar'
    restore_link.allow_tags = True
    
