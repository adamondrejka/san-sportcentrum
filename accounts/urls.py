# -*- coding: utf-8 -*- 
from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()
from administration.views import VoucherList, VoucherCreate, VoucherUpdate, VoucherDelete, SportovisteList, SportovisteCreate, SportovisteUpdate, SportovisteDelete, SportovniCentrumList, SportovniCentrumCreate, SportovniCentrumUpdate, SportovniCentrumDelete, RezervaceDelete, RezervaceDetail, RezervaceList


urlpatterns = patterns('',
    # Examples:
    url(r'^login/$', 'accounts.views.login_view', name='accounts-login'),
    url(r'^logout/$', 'accounts.views.logout_view', name='accounts-logout'),
    url(r'^activate/$', 'accounts.views.activate_account_view', name='accounts-activate'),
    url(r'^registration/$', 'accounts.views.registration_view', name='accounts-registration'),

)

