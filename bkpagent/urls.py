# -*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('bkpagent.views',
    url(r'^register/$', 'register_to_server'),
    #url(r'^get_header/$', 'get_header'),
    #url(r'^log/(?P<machine_id>)/$', 'post_log'),
)
