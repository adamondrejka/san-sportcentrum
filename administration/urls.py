# -*- coding: utf-8 -*- 
from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()
from administration.views import VoucherList, VoucherCreate, VoucherUpdate, VoucherDelete, SportovisteList, SportovisteCreate, SportovisteUpdate, SportovisteDelete, SportovniCentrumList, SportovniCentrumCreate, SportovniCentrumUpdate, SportovniCentrumDelete, RezervaceDelete, RezervaceDetail, RezervaceList, UzivatelList, UzivatelCreate, UzivatelUpdate, UzivatelDelete


urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'administration.views.home_view', name='admin-home'),
    url(r'^vouchery/$', VoucherList.as_view(), name='admin-vouchery'),
    url(r'^voucher/add/$', VoucherCreate.as_view(), name='admin-voucher-create'),
    url(r'^voucher/(?P<pk>\d+)/$', VoucherUpdate.as_view(), name='admin-voucher-update'),
    url(r'^voucher/delete/(?P<pk>\d+)/$', VoucherDelete.as_view(), name='admin-voucher-delete'),

    url(r'^sportoviste/$', SportovisteList.as_view(), name='admin-sportoviste'),
    url(r'^sportoviste/add/$', SportovisteCreate.as_view(), name='admin-sportoviste-create'),
    url(r'^sportoviste/(?P<pk>\d+)/$', SportovisteUpdate.as_view(), name='admin-sportoviste-update'),
    url(r'^sportoviste/delete/(?P<pk>\d+)/$', SportovisteDelete.as_view(), name='admin-sportoviste-delete'),

    url(r'^sportovni-centra/$', SportovniCentrumList.as_view(), name='admin-sportovnicentra'),
    url(r'^sportovni-centrum/add/$', SportovniCentrumCreate.as_view(), name='admin-sportovnicentrum-create'),
    url(r'^sportovni-centrum/(?P<pk>\d+)/$', SportovniCentrumUpdate.as_view(), name='admin-sportovnicentrum-update'),
    url(r'^sportovni-centrum/delete/(?P<pk>\d+)/$', SportovniCentrumDelete.as_view(), name='admin-sportovnicentrum-delete'),

    url(r'^rezervace/$', RezervaceList.as_view(), name='admin-rezervace'),
    url(r'^rezervace/(?P<pk>\d+)/$', RezervaceDetail.as_view(), name='admin-rezervace-detail'),
    url(r'^rezervace/delete/(?P<pk>\d+)/$', RezervaceDelete.as_view(), name='admin-rezervace-delete'),

    url(r'^uzivatele/$', UzivatelList.as_view(), name='admin-uzivatele'),
    url(r'^uzivatel/add/$', UzivatelCreate.as_view(), name='admin-uzivatel-create'),
    url(r'^uzivatel/(?P<pk>\d+)/$', UzivatelUpdate.as_view(), name='admin-uzivatel-update'),
    url(r'^uzivatel/delete/(?P<pk>\d+)/$', UzivatelDelete.as_view(), name='admin-uzivatel-delete'),
    url(r'^uzivatel/delete/(?P<pk>\d+)/$', UzivatelDelete.as_view(), name='admin-uzivatel-delete'),

    url(r'^vouchers-generate/$', 'administration.views.generate_vouchers', name='admin-voucher-generate'),
)

