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
    files = models.TextField(verbose_name='arquivos')
    destination = models.CharField(verbose_name='destino', max_length=80)
    successful = models.BooleanField(verbose_name='status')
    
    class Meta:
        verbose_name = u'histórico'
        
    def __unicode__(self):
        return str(self.dump_date)

