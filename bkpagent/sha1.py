# -*- coding: utf-8 -*-
'''
Created on 17/11/2012

@author: gustavo
'''

def sha1_hexdigest(filename):
    from datetime import datetime
    dt1 = datetime.now()
    import hashlib
    sha1 = hashlib.sha1();
    if isinstance(filename, str):
        with open(filename, 'rb') as f:
            for data in iter(lambda: f.read(8192), b''):
                sha1.update(data)
        dt2 = datetime.now()
        print str(dt2 - dt1)
        return sha1.hexdigest()

def blah():
    from bkpagent.sha1 import sha1_hexdigest
    sha1_hexdigest('/media/Linux/VÍDEO CURSO LINGUAGEM SQL - Proj. Banco de Dados/Cap03 - Projeto de Banco de Dados.mkv' )
