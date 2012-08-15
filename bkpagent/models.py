# -*- coding: utf-8 -*-

from django.db import models
from django.template.defaultfilters import slugify

class ThisMachine(models.Model):
    name = models.CharField(max_length=80)
    slug = models.SlugField(max_length=80)
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(ThisMachine, self).save(*args, **kwargs)
        
class Server(models.Model):
    name = models.CharField(max_length=80)
    configpath = models.CharField(max_length=1024)
    port = models.CharField(max_length=5)

class BackupHistory(models.Model):
    dump_date = models.DateTimeField(verbose_name='data')
    filename = models.CharField(verbose_name='arquivo', max_length=1024)
    destination = ForeignKey('Destination', verbose_name='destino')
    local_ok = models.BooleanField(verbose_name='backup local')
    remote_ok = models.BooleanField(verbose_name='backup remoto')
    files_transfered = models.TextField(verbose_name='arquivos transferidos')
    
    class Meta:
        verbose_name = u'histórico'
        
    def __unicode__(self):
        return str(self.dump_date)

class Destination(models.Model):
    u"""
        name = nome específico do destino. Padrão preferível: "Projeto - Máquina" (ex.: "Sapem - Gruyere")
        full_address = endereço completo de destino (<user>@<address>:<dir>)
        port = porta aberta para acesso SSH
    """
    name = models.CharField(max_length=80, verbose_name='nome')
    full_address = models.CharField(max_length=512, verbose_name=u'endereço')
    port = models.CharField(max_length=5, verbose_name='porta')
    
    class Meta:
        verbose_name = 'servidor'
        verbose_name_plural = 'servidores'
        ordering = ['name']
    
    def __unicode__(self):
        return self.name
