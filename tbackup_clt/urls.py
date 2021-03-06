from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.views.generic.simple import direct_to_template
#import django_cron
#django_cron.autodiscover()
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls), name='admin'),
    url(r'^$', direct_to_template, {'template': 'index.djhtml'}, name='home'),
    #url(r'^admin/doc/', include('django.contrib.admindocs.urls'), name='admindocs'),
    #url(r'^tbackup_server/', include('tbackup_server.urls'), {}, name="tbackup-server",),
    url(r'^tbackup_client/', include('tbackup_client.urls'), {}, name='tbackup-client'),
)
