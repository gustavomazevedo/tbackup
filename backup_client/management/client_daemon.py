from django.core.management.base import BaseCommand, CommandError
from backup_client.models import Config, Server

class Command(BaseCommand):
    help = 'Updates configuration file and sets up backup jobs'
    
    def handle(self):
        try:
            config_file = get_config_file()
        except:
            raise CommandError('Could not connect to server')
        
        try:    
            config = Config.objects.get(name=config_file.name)
        except Config.DoesNotExist:   
            config = Config(name=config_file_name)
            
        config.content = config_file
            







def get_config_file():
    server = Server.objects.get(pk=1)
    return server.cmd_config
