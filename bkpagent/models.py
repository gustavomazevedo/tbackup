# -*- coding: utf-8 -*-

from django.db import models


class Server(models.Model):
    name = models.CharField(max_length=80)
    configpath = models.CharField(max_length=1024)
    port = models.CharField(max_length=5)

class BackupHistory(models.Model):
    dump_date = models.DateTimeField(verbose_name='data')
    files = models.TextField(verbose_name='arquivos')
    destination = models.CharField(verbose_name='destino')
    successful = models.BooleanField(verbose_name='status')

