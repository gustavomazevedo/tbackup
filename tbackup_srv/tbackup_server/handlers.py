# -*- coding: utf-8 -*-

from django.utils import simplejson as json
import logging

def exception_handler(func):
    def wrap(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except:
            logging.exception('server: falha na view %s' % func.__name__)
            import traceback
            ex_msg = traceback.print_exc(file=open('/home/gustavo/errorlog.txt','a'))
            logging.exception(ex_msg)
            server_info = {'exception' : ex_msg}
            message = { 'error' : True,
                        'value' : json.dumps(server_info)}
            return message
        
    return wrap