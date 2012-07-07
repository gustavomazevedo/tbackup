# -*- coding: utf-8 -*-

from django.db import models


class Server(models.Model):
    name = models.CharField(max_length=80)
    configpath = models.CharField(max_length=1024)
    port = models.CharField(max_length=5)
