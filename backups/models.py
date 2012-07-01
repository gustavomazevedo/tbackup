from django.db import models

# Create your models here.
from tbackup.usermachines import Maquina, Diretorio

class Backup(models.Model):
    maquina = models.ForeignKey(Maquina)
    caminho = models.ForeignKey(Diretorio)
    CharField()
    nome = models.CharField()
    filename = models.CharField()
    fileobj = models.FileField()
