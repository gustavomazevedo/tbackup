# -*- coding: utf-8 -*-

from django import forms
from django.db import models
#from models import PERIODICIDADE_CHOICES, Maquina, Usuario, Diretorio, Credencial, Transferencia
from bkpserver.models import Origin, Destination, Transfer
#from bkpserver.timedeltafield import TimedeltaFormField


class DestinationForm(forms.ModelForm):
    name = forms.CharField(max_length=80, required=True)
    full_address = forms.CharField(max_length=512, required=True)
    port = forms.CharField(max_length=5, required=True)
    
    class Meta:
        model = Destination

class TransferForm(forms.ModelForm):
    origin  = forms.ModelChoiceField(
        queryset=Origin.objects.all(),
        required=True,
    )
    destination = forms.ModelChoiceField(
        queryset=Destination.objects.all(),
        required=True, 
    )
    delta = TimedeltaFormField(required=True)

    class Meta:
        model = Transfer

