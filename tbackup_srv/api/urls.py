# -*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('api.handlers',
    url(r'^register/$', 'register'),
    url(r'^log/(?P<machine_id>)/$', 'post_log'),
    url(r'^recover/$','recover'),
    
)
