# -*- coding: utf-8 -*- 
from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'web.views.home_view', name='home'),
    url(r'^rezervace/$', 'web.views.rezervace_view', name='rezervace'),
    url(r'^kontakt/$', 'web.views.kontakt_view', name='web-kontakt'),
    url(r'^o-nas/$', 'web.views.onas_view', name='web-onas'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)

