from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'tbackup.views.home', name='home'),
    # url(r'^tbackup/', include('tbackup.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    #url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    #url(r'^logs/', 'tbackup.logs.views.index'),
    #url(r'^machines/', 'tbackup.machines.views.index'),
    #url(r'^bkpclient/', include('bkpclient.urls')),
    url(r'^bkpserver/', include('bkpserver.urls')),
    #url(r'^usermachines/', 'tbackup.usermachines.views.index'),
)
