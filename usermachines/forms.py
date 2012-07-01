# -*- coding: utf-8 -*-

from django import forms
from django.db import models
from models import DIAS_SEMANA, Maquina, Usuario, Diretorio, Credencial, Transferencia


class DiretorioForm(forms.ModelForm):
    maquina = forms.ModelChoiceField(
        queryset=Maquina.objects.all()
    )
    caminho = forms.CharField(max_length=1024, initial='/home/')
            
    class Meta:
        model = Diretorio

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario

class MaquinaForm(forms.ModelForm):
    class Meta:
        model = Maquina
        
class CredencialForm(forms.ModelForm):
    class Meta:
        model = Credencial


class TransferenciaForm(forms.ModelForm):

    origem  = forms.ModelChoiceField(
        queryset=Credencial.objects.exclude(chave_ssh__exact=''),
        required=True, 
        label=u'Origem'
    )
    origem_dir = forms.ChoiceField(required=True, label=u'Diretório na origem')

    destino = forms.ModelChoiceField(
        queryset=Credencial.objects.exclude(maquina__endereco__exact='').exclude(maquina__porta__exact=''),
        required=True, 
        label='Destino'
    )
    destino_dir = forms.ChoiceField(required=True, label=u'Diretório no destino')

    horario = forms.TimeField(required=True, label=u'Horário')

    dias = forms.MultipleChoiceField(
        required=True, 
        label=u'Dias', 
        choices=DIAS_SEMANA, 
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Transferencia

    #class Media:
    #    js = ('http://ajax.googleapis.com/ajax/libs/jquery/1.4.0/jquery.min.js','site_media/js/dir.js')

