from django.contrib import admin

from tbbackup.logs.models import LogHistory, ArquivoBackup

class LogHistoryAdmin(admin.ModelAdmin):
	fields = ('arquivos','status', 'data')
	list_display  = ('nomes_dos_arquivos','status','data')
	list_filter   = ('data',)
	
admin.site.register(LogHistory, LogHistoryAdmin)

