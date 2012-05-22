# -*- coding: utf-8 -*-

from django.db import models

# Create your models here.

STATUS_CHOICES = (
        (0,'ERRO'),
        (1,'OK'),
    )

backups = 'backups/'
    
class LogHistory(models.Model):
    arquivos = models.ManyToManyField('ArquivoBackup', verbose_name='lista de arquivos')
    data     = models.DateTimeField()
    status   = models.IntegerField(choices=STATUS_CHOICES)

    def get_arquivos(self):
        return self.arquivos.all()

    def nomes_dos_arquivos(self):
        return '\n'.join([x.nome for x in self.arquivos.all()])
    
    def getPrettyHTML(self, fieldName):
        val = getattr(self, fieldName)
        if fieldName == 'arquivos':
            return '\n'.join([x.nome for x in val.all()])
        elif fieldName == 'data':
            return u'%02d/%02d/%04d às %02d:%02d' % (val.day, val.month, val.year, val.hour, val.minute)
        elif fieldName == 'status':
            if val: return 'OK'
            else: return 'ERRO'
        return val
    
    def get_fields(self):
        return [(field.value_to_string(self)) for field in self._meta.fields]
    
    class Meta:
        verbose_name = u'histórico de log'
    
    def __unicode__(self):
        val = getattr(self, 'data')
        return u'%02d/%02d/%04d às %02d:%02d' % (val.day, val.month, val.year, val.hour, val.minute)

class ArquivoBackup(models.Model):
    nome    = models.CharField(max_length=300, blank=False)
    arquivo = models.FileField("Arquivo de backup", upload_to=backups)
	
    def __unicode__(self):
        return self.nome

#class LogHistoryForm(forms.ModelForm):
#    class Meta:
#        model = LogHistory
    
