# -*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('bkpserver.views',
    url(r'^config/(?P<machine_id>)/$', 'get_config_file'),
    url(r'^log/(?P<machine_id>)/$', 'post_log'),
)
