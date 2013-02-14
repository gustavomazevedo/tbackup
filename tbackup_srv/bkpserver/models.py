# -*- coding: utf-8 -*-

from django.db import models
from django import forms
from django.forms import widgets
from django.template.defaultfilters import slugify

from . import TIMEDELTA_CHOICES

class Origin(models.Model):
    u"""
        name = nome específico da origem
    """
    name = models.CharField(max_length=80, verbose_name='nome')
    sshkey = models.TextField(verbose_name='chave ssh')
    slug = models.SlugField(max_length=80)
    
    class Meta:
        verbose_name = 'origem'
        verbose_name_plural = 'origens'
        ordering = ['name']
    
    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.pk:
            self.slug = slugify(self.name)
        models.Model.save(self, *args, **kwargs)

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

class Transfer(models.Model):
    u"""
        par único:
        (
        origin = máquina de origem
        destination = servidor de backup de destino
        )
        delta = periodicidade do backup   
            
    """
    origin = models.ForeignKey(Origin, verbose_name='origem')
    destination = models.ForeignKey(Destination, verbose_name='destino')
    delta = models.CharField(max_length=6, verbose_name='periodicidade')
    #delta_type = models.CharField(max_length=1,choices=TIMEDELTA_CHOICES)
    
    class Meta:
        verbose_name = u'transferência'
        ordering = ['origin__name','destination__name']
    
    def __unicode__(self):
        return self.origin.name + " => " + self.destination.name
        
class BackupHistory(models.Model):
    origin = models.ForeignKey(Origin)
    dump_date = models.DateTimeField(verbose_name='data')
    files = models.TextField(verbose_name='arquivos')
    destination = models.CharField(verbose_name='destino', max_length='80')
    successful = models.BooleanField(verbose_name='status')
    
    class Meta:
        verbose_name = u'histórico'
        ordering = ['origin__name','-dump_date']
        
#    def __unicode__(self):
#        return self.origin.name + ""
      
class DestinationForm(forms.ModelForm):
    class Meta:
        model = Destination

class TimedeltaWidget(widgets.MultiWidget):
    def __init__(self, attrs=None):
        widget = (
            widgets.TextInput(attrs={'size': 3, 'maxlength': 3}),
            widgets.Select(choices=TIMEDELTA_CHOICES),
            )
        super(TimedeltaWidget, self).__init__(widget, attrs=attrs)
        
    def decompress(self, value):
        if value:
            return [value[:-1], value[-1]]
        return [None, None]
    
    def format_output(self, rendered_widgets):
        return u''.join(rendered_widgets)

class TimedeltaFormField(forms.MultiValueField):
    widget = TimedeltaWidget
    
    def __init__(self, *args, **kwargs):
        fields = (
            forms.IntegerField(),
            forms.ChoiceField(choices=TIMEDELTA_CHOICES),
        )
        super(TimedeltaFormField, self).__init__(fields, *args, **kwargs)
    
    def compress(self, data_list):
        if data_list:
            return str(data_list[0]) + data_list[1]
        return ''

        
class TransferForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(TransferForm, self).__init__(*args, **kwargs)
        self.fields['delta'] = TimedeltaFormField(label=self.fields['delta'].label,*args, **kwargs)

    class Meta:
        model = Transfer


