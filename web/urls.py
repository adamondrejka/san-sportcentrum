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
    url(r'^vouchery/$', 'web.views.vouchery_view', name='web-vouchery'),
    url(r'^kredit/$', 'web.views.kredit_view', name='web-kredit'),
    url(r'^cancel_reservation/$', 'web.views.cancel_reservation', name='web-cancel-reservation'),
    url(r'^ajax/get_sportoviste/$', 'web.views.ajax_get_sportoviste', name='ajax-get-sportoviste'),
    url(r'^ajax/get_calendar/$', 'web.views.ajax_get_table_calendar', name='ajax-get-table-calendar'),
    url(r'^ajax/make_reservation/$', 'web.views.ajax_make_reservation', name='ajax-make-reservation'),
    url(r'^ajax/pay/$', 'web.views.ajax_pay', name='ajax-pay'),
    url(r'^ajax/delete_reservation/$', 'web.views.ajax_delete_rezervace', name='ajax-delete-rezervace'),
)

