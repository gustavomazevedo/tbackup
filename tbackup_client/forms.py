# -*- coding: utf-8 -*-

from django.forms import widgets
from django import forms

from tbackup_client.models import Config

INTERVALTYPE_CHOICES = (
                        (60, 'horas'),
                        (1440,'dias'),
                        (10080,'semanas'),
                        (21600,'quinzenas'),
                    )

class TimedeltaWidget(widgets.MultiWidget):
    def __init__(self, attrs=None):
        widget = (
            widgets.TextInput(attrs={'size': 3, 'maxlength': 3}),
            widgets.Select(choices=INTERVALTYPE_CHOICES),
            )
        super(TimedeltaWidget, self).__init__(widget, attrs=attrs)
        
    def decompress(self, value):
        if value:
            for div, name in reversed(INTERVALTYPE_CHOICES):
                if value % div == 0:
                    return [value / div, name]
        return [None, None]
    
    def format_output(self, rendered_widgets):
        return u''.join(rendered_widgets)

class TimedeltaFormField(forms.MultiValueField):
    widget = TimedeltaWidget
    
    def __init__(self, *args, **kwargs):
        fields = (
            forms.IntegerField(),
            forms.ChoiceField(choices=INTERVALTYPE_CHOICES),
        )
        super(TimedeltaFormField, self).__init__(fields, *args, **kwargs)

    def compress(self, data_list):
        if data_list:
            return data_list[0] * data_list[1]
        return ''

#class AlfaNumericFormField(forms.CharField):
#    def clean(self, value):
#        import re
#        from django.forms import ValidationError
#        value = super(AlfaNumericFormField, self).clean(value)
#        if not re.match(r'^[A-Za-z][A-Za-z0-9_.]+', value):
#            raise ValidationError(u'Primeiro dígito deve ser letra, subsequentes podem ser alfanuméricos e os símbolos "_" (underscore) e "." (ponto)')
        
class ConfigForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ConfigForm, self).__init__(*args, **kwargs)
        self.fields['interval'] = TimedeltaFormField(
                                label=self.fields['interval'].label,
                                *args, **kwargs)

    class Meta:
        model = Config
        
class RegisterForm(forms.Form):
    origin_name = forms.RegexField(
	    max_length=80,
		label=u'ID', 
		regex=r'^[A-Za-z][A-Za-z0-9_.]*',
		error_message=u'Primeiro caractere deve ser obrigatoriamente uma letra.\n' +
					  u'Subsequentes podem ser alfanuméricos, ou os símbolos _ e .')