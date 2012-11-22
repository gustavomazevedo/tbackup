# -*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('tbackup_client.views',
    url(r'^$', 'index', name='tbackup-client'),
    url(r'^register/$', 'register'),
    url(r'^log/$','log'),
    url(r'^config/$','config'),
    #url(r'^api/name_available/$','name_available'),
    #url(r'^get_header/$', 'get_header'),
    #url(r'^log/(?P<machine_id>)/$', 'post_log'),
    #url(r'^recover/$','recover'),
)
