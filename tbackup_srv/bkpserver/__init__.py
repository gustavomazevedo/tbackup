# -*- coding: utf-8 -*-
import os.path
from django.conf import settings

TIMEDELTA_CHOICES = (
    ('h','horas'),
    ('d','dias'),
    ('s','semanas'),
    ('q','quinzenas'),
)

HOURS_MULTIPLIER = {
    'h': 1,
    'd': 24,
    's': 168,
    'q': 360,
}

HEADER_CONFIG_FILE = {
    'header': {
        'srv_name' : 'Gruyere - LPS',
        'srv_address' : 'gustavo@gruyere.lps.ufrj.br',
        'srv_port' : 22,
        'admins' : getattr(settings,'ADMINS'),
        'cfg_path': '{}/tb/tbackup/configs/origin_name.cfg'.format(os.path.expanduser("~")),
    }
}

def header(origin_name):
    h = HEADER_CONFIG_FILE
    h['header']['cfg_path'] = h['header']['cfg_path'].replace('origin_name',origin_name)
    return h
