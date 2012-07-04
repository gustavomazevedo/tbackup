# -*- coding: utf-8 -*-

from django.db import models


class Server(models.Model):
    name = models.CharField(max_length=80)
    address = models.CharField(max_length=1024)
    
