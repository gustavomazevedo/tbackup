# -*- coding: utf-8 -*-

from django.db import models
from django    import forms

from smart_selects.db_fields import ChainedForeignKey

DAYS_CHOICES = (
    ('1','Domingo'),
    ('2','Segunda'),
    ('3','Terça'),
    ('4','Quarta'),
    ('5','Quinta'),
    ('6','Sexta'),
    ('7','Sábado'),
)

class Machine(models.Model):
    nome = models.CharField(max_length=256)
    user = models.ForeignKey('SystemUser')
    user = models.CharField(max_length=256)
    dirs = models.TextField(verbose_name=u'Diretórios')

    class Meta:
        abstract = True
        verbose_name = u'máquina'
        ordering = ['nome']

    def __unicode__(self):
        return getattr(self,'user') + ' @ ' + getattr(self, 'nome')

    def get_fields(self):
        return [(field.value_to_string(self)) for field in self._meta.fields]


class Origin(Machine):
    sshkey   = models.TextField()

    class Meta:
        verbose_name = 'Origem'
        verbose_name_plural = 'Origens'

class Destination(Machine):
    endereco = models.CharField(verbose_name = u'Endereço',max_length=256)
    porta    = models.CharField(max_length=4)

    class Meta:
        verbose_name = 'Destino'

class SystemUser(models.Model):
    username = models.CharField(max_length=256)

    class Meta:
        verbose_name = 'usuário'

    def __unicode__(self):
        return username

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

class Transfer(models.Model):
    origin     = models.ForeignKey(Origin)
    origin_dir = models.FilePathField(max_length=1024)

    destination     = models.ForeignKey(Destination)
    destination_dir = models.FilePathField(max_length=1024)

    horario = models.TimeField()
    #dias    = models.ManyToManyField('DayChoices')
    dias    = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Transferência'


class TransferForm(forms.ModelForm):

    origin  = forms.ModelChoiceField(queryset=Origin.objects.all(),required=True, label=u'Origem')
    #try:
    #o = Origin.objects.get(pk=1)
    #origin_dir = forms.ChoiceField(required=True, label=u'Diretório na origem',choices=[(x,x) for x in o.dirs.replace('\r','').split('\n')])
    #except:
    origin_dir = forms.ChoiceField(required=True, label=u'Diretório na origem')

    destination     = forms.ModelChoiceField(queryset=Destination.objects.all(),required=True, label='Destino')

    #try:
    #d = Destination.objects.get(pk=1)
    #destination_dir = forms.ChoiceField(required=True, label=u'Diretório no destino',choices=[(x,x) for x in d.dirs.replace('\r','').split('\n')])
    #except:
    destination_dir = forms.ChoiceField(required=True, label=u'Diretório no destino')

    horario = forms.TimeField(required=True, label=u'Horário')
    #dias    = forms.ModelMultipleChoiceField(queryset=DayChoices.objects.all(),required=True, label=u'Dias', widget=forms.CheckboxSelectMultiple)
    dias    = forms.MultipleChoiceField(required=True, label=u'Dias', choices=DAYS_CHOICES, widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Transfer

