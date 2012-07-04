from django.contrib import admin

from django.core import serializers
from django.http import HttpResponse, HttpResponseBadRequest

from models import Maquina, Diretorio, Usuario, Credencial, Transferencia
from forms import MaquinaForm, DiretorioForm, UsuarioForm, CredencialForm, TransferenciaForm


class DiretorioAdmin(admin.ModelAdmin):
    form = DiretorioForm

class MaquinaAdmin(admin.ModelAdmin):
    form = MaquinaForm

class UsuarioAdmin(admin.ModelAdmin):
    form = UsuarioForm

class CredencialAdmin(admin.ModelAdmin):
    form = CredencialForm
    list_filter   = ('maquina__nome','usuario__nome')

class TransferenciaAdmin(admin.ModelAdmin):
    form = TransferenciaForm
    #fields = ('origin','origin_dir','destination','destination_dir','horario')
    #class Media:
    #    js = ('http://ajax.googleapis.com/ajax/libs/jquery/1.4.0/jquery.min.js','site_media/js/dir.js')


def get_dirs(request):
    if request.is_ajax():
        usermachine = request.GET.get('origin')
        if usermachine is None:
            usermachine = request.GET.get('destination')
        
        username = usermachine.split('@')[0]
        machname = usermachine.split('@')[1]
        m = Maquina.objects.get(nome=machname)
        dirs = Diretorio.objects.get(machine=m).get(caminho__contains='/home/' + username)
        response = serializers.serialize("json", dirs)
        return HttpResponse(response, mimetype="text/javascript")
    else:
        return HttpResponseBadRequest()

admin.site.register(Maquina, MaquinaAdmin)
admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(Diretorio, DiretorioAdmin)
admin.site.register(Credencial, CredencialAdmin)
admin.site.register(Transferencia, TransferenciaAdmin)

