# -*- coding: utf-8 -*-

from django.contrib import admin
from django.utils import simplejson as json

from bkpserver.models import Origin, Destination, Transfer, DestinationForm, TransferForm

from . import header, HEADER_CONFIG_FILE

class OriginAdmin(admin.ModelAdmin):
    exclude = ('sshkey',)
    list_filter =('name',)

    def has_add_permission(self, request):
        return False

    def has_change_permission(self,request):
        return False


class DestinationAdmin(admin.ModelAdmin):
    form = DestinationForm

class TransferAdmin(admin.ModelAdmin):
    form = TransferForm

    def save_model(self, request, obj, form, change):
        obj.save()
        make_config_file(obj.origin__name)
        authorize_key(obj.origin)

def make_config_file(origin_name):
    config = []
    header_dict = header(origin_name)
    config.append(header_dict)

    time = datetime.now()
    time -= timedelta(minutes=time.minute, seconds=time.second, microseconds=time.microseconds)

    tranfers = Transfer.objects.get(origin__name=origin_name)
    for t in transfers:
        d = t.destination
        c = {
            'backup' : {
                'nome_destino': d.name,
                'destino': d.full_address,
                'periodicidade': parse_delta(t.delta),
                'primeiro_backup': str(time),
            }
        }
        config.append(c)
    cf = json.dumps(config)
    f = open(header_dict['header']['cfg_path'],'w')
    f.write(cf + '\n')
    f.close()

#def authorize_key(pk):


def parse_delta(delta):
    if delta[-1] == 'h':
        hours = int(delta[:-1])
        return str(hours / 24) + 'd' + str(hours % 24) + 'h'
    elif delta[-1] == 'd':
        return delta
    elif delta[-1] == 's':
        weeks = int(delta[:-1])
        return str(weeks * 7) + 'd'
    elif delta[-1] == 'q':
        fortnights = int(delta[:-1])
        return str(fortnights * 15) + 'd'


admin.site.register(Origin, OriginAdmin)
admin.site.register(Destination, DestinationAdmin)
admin.site.register(Transfer, TransferAdmin)


#def get_dirs(request):
#    if request.is_ajax():
#        usermachine = request.GET.get('origin')
#        if usermachine is None:
#            usermachine = request.GET.get('destination')
#        
#        username = usermachine.split('@')[0]
#        machname = usermachine.split('@')[1]
#        m = Maquina.objects.get(nome=machname)
#        dirs = Diretorio.objects.get(machine=m).get(caminho__contains='/home/' + username)
#        response = serializers.serialize("json", dirs)
#        return HttpResponse(response, mimetype="text/javascript")
#    else:
#        return HttpResponseBadRequest()

#admin.site.register(Maquina, MaquinaAdmin)
#admin.site.register(Usuario, UsuarioAdmin)
#admin.site.register(Diretorio, DiretorioAdmin)
#admin.site.register(Credencial, CredencialAdmin)
#admin.site.register(Transferencia, TransferenciaAdmin)

