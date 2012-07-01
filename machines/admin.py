from django.contrib import admin

from tbackup.machines.models import Origin, Destination, Transfer, OriginForm, DestinationForm, TransferForm

class MachineAdmin(admin.ModelAdmin):
    list_filter   = ('nome','user')

class OriginAdmin(MachineAdmin):
    form = OriginForm
    #fields = ('nome','user', 'dirs','sshkey')

class DestinationAdmin(admin.ModelAdmin):
    form = DestinationForm
    #fields = ('nome','user', 'dirs','endereco','porta')

class TransferAdmin(admin.ModelAdmin):
    form = TransferForm
    #fields = ('origin','origin_dir','destination','destination_dir','horario')
    #class Media:
    #    js = ('http://ajax.googleapis.com/ajax/libs/jquery/1.4.0/jquery.min.js','site_media/js/dir.js')

admin.site.register(Origin, OriginAdmin)
admin.site.register(Destination, DestinationAdmin)
admin.site.register(Transfer, TransferAdmin)

