# -*- coding: utf-8 -*-

from django.db import models

from datetime import datetime
# Create your models here.

class DummyData(models.Model):
    name = models.CharField(max_length=80)
    type = models.CharField(max_length=20)
    date = models.DateTimeField(default=datetime.now())