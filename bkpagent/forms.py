# -*- coding: utf-8 -*-

from django import forms

class ThisMachineForm(forms.Form):
    name = forms.CharField(max_length=80, label=u'nome para identificar este computador')
