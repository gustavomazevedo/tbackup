
import subprocess
import gzip

from datetime import date, datetime

import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'tbbackup.settings'

from tbbackup.logs.models import LogHistory, ArquivoBackup



class BackupClass():

    def __init__(self, zip_src,zip_dest,rsync_dest,is_ssh=None,port=None):
        self.zip_src    = zip_src
        self.zip_dest   = zip_dest
        self.rsync_src  = '/'.join(zip_dest.split('/')[0:-2])
        self.rsync_dest = rsync_dest
        self.is_ssh     = is_ssh
        self.port       = port

    def execute(self):
        if not os.path.exists(self.zip_dest):
            self.zipfiles()
        stdout, stderr = self.rsync()
        filenameList = stdout.split('\n')[1:-4]
        self.writeToModel(filenameList, stderr)
    
    def zipfiles(self):
        f_in  = open(self.zip_src, 'rb')
        f_out = gzip.open(self.zip_dest,'wb',9)
        f_out.writelines(f_in)
        f_out.close()
        f_in.close()

    def rsync(self):
        if self.is_ssh:
            sshStr = '-e "ssh -p ' + str(self.port) + '" '
        else:
            sshStr = ''
        sync = subprocess.Popen(('/usr/bin/rsync ' + sshStr + '-avz' + self.rsync_src + ' ' + self.rsync_dest).split(),
                                 shell=False,
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)
        return sync.communicate()

    def writeToModel(self, filenameList, standardError):
        logEntry = LogHistory(data=datetime.now())
        
        #if standardError:
        #    logEntry.status = 0 #ERRO
        #    arquivo, wasCreated = ArquivoBackup.objects.get_or_create(nome='nenhum arquivo copiado')
        #    arquivo.save()
        #    logEntry.arquivos.add(arquivo)
        #    logEntry.save()
        #    return
        
        logEntry.status = 1 #OK
        
        if len(filenameList) == 0:
            logEntry.save()
            arquivo, wasCreated  = ArquivoBackup.objects.get_or_create(nome='nenhum arquivo copiado')
            arquivo.save()
            logEntry.arquivos.add(arquivo)
            return
        
        for f in filenameList:
            logEntry.save()
            arquivo, wasCreated = ArquivoBackup.objects.get_or_create(nome=f)
            arquivo.save()
            logEntry.arquivos.add(arquivo)
            
backup = BackupClass(
    zip_src    = '/usr/lib/projetotb/sapem/sapem/tbForms/tb.db',
    zip_dest   = '/home/projetotb/backup/sapem.' + str(date.today()) + '.db.gz',
    rsync_dest = 'srvupt.hucff.ufrj.br:~/sapem/',
    is_ssh     = True,
    port       = 8
)
backup.execute()

backup.rsync_dest = 'neuraltb@loghost02.lps.ufrj.br:~/sapem/'
backup.port = 22
backup.execute()
