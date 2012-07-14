# -*- coding: utf-8 -*-

from django.db import models

PERIODICIDADE_CHOICES = (
    ('m','meses'),
    ('w','semanas'),
    ('d','dias'),
    ('H','horas'),
)

class Maquina(models.Model):
    nome     = models.CharField(max_length=256)
    endereco = models.CharField(verbose_name = u'Endereço',max_length=256, blank=True)
    porta    = models.CharField(max_length=5, blank=True)
    
    class Meta:
        verbose_name = u'Máquina'
        ordering = ['nome']

    def __unicode__(self):
        return getattr(self, 'nome')
        
class Diretorio(models.Model):
    maquina = models.ForeignKey(Maquina)
    caminho = models.CharField(max_length=1024)

    class Meta:
        verbose_name =u'Diretório'
        ordering = ['caminho']
        
    def __unicode__(self):
        return getattr(self,'caminho')

class Usuario(models.Model):
    maquina = models.ForeignKey(Maquina)
    nome    = models.CharField(max_length=50, verbose_name = u'Nome de usuário')

    class Meta:
        verbose_name = u'Usuário'

    def __unicode__(self):
        return getattr(self,'nome')

class Credencial(models.Model):
    maquina   = models.ForeignKey(Maquina)
    usuario   = models.ForeignKey(Usuario)
    chave_ssh = models.TextField(verbose_name=u'Chave SSH', blank=True)

    class Meta:
        verbose_name = u'Credencial'    
        verbose_name_plural = u'Credenciais'
                
    def __unicode__(self):
        return getattr(self,'usuario') + '@' + getattr(self,'maquina')
        
class Transferencia(models.Model):
    origem = models.ForeignKey(Credencial, related_name='transferencia_origem_set')
    origem_dir = models.FilePathField(max_length=1024)
    destino = models.ForeignKey(Credencial, related_name='transferencia_destino_set')
    destino_dir = models.FilePathField(max_length=1024)
    primeirobkp = models.DateTimeField()
    periodicidade = models.BigIntegerField()
    period_tipo = models.CharField(max_length=1, choices=PERIODICIDADE_CHOICES)

    class Meta:
        verbose_name = 'Transferência'

        
        
"""
class OriginForm(forms.ModelForm):
    nome = forms.CharField(max_length=256)
    user = forms.CharField(max_length=256)
    dirs = forms.CharField(widget=forms.Textarea, help_text=u'digitar cada diretório em uma nova linha')
    sshkey = forms.CharField(widget=forms.Textarea, label='Chave SSH', help_text = u'Chave para acesso remoto localizada em ~/.ssh/id_rsa.pub')

    class Meta:
        model = Origin

class DestinationForm(forms.ModelForm):
    nome = forms.CharField(required=True, max_length=256)
    user = forms.CharField(required=True, max_length=256)
    dirs = forms.CharField(required=True, widget=forms.Textarea, help_text=u'digitar cada diretório em uma nova linha')
    endereco = forms.CharField(required=True, label=u'Endereço',max_length=256)
    porta = forms.CharField(required=True, max_length=4)

    class Meta:
        model = Destination
"""


