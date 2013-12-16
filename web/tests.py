# -*- coding: utf-8 -*-
"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
import datetime
from django.core.urlresolvers import reverse

from django.test import TestCase, Client
from model_mommy import mommy
from core.models import Rezervace, Sportoviste, User, SportovisteMisto, Voucher


class MakeReservationTest(TestCase):
    def setUp(self):
        self.reservation = mommy.make(Rezervace)
        self.misto = mommy.make(SportovisteMisto)
        self.misto.sportoviste.cena_interval = 200
        self.misto.sportoviste.interval_vypujcek = datetime.time(hour=0, minute=30)
        self.misto.sportoviste.save()
        self.user = mommy.make(User)
        self.user.konto = 10000
        self.user.save()

        self.client = Client()
        self.url = reverse('ajax-make-reservation')

        self.request = {
            'zakaznik': self.user.id,
            'misto': self.misto.id,
            'rezervace_datum': '2013-12-16',
            'rezervace_od': 180,
            'rezervace_do': 240,
            'sportoviste_misto': self.misto.id
        }

    def test_new_reservation(self):
        """
        Tests that creating new reservation work
        """
        response = self.client.post(self.url, self.request)
        self.assertContains(response, 'ok', status_code=200)

    def test_no_money(self):
        """
        Tests that user hasn't got enough money
        """

        self.user.konto = 100
        self.user.save()

        response = self.client.post(self.url, self.request)
        self.assertContains(response, 'nomoney', status_code=200)

    def test_update_reservation(self):
        """
        Tests that reservation will update succesfully
        """
        self.request['rezervace_id'] = self.reservation.id
        self.request['stav'] = 2

        response = self.client.post(self.url, self.request)
        self.assertContains(response, 'ok', status_code=200)

        updated_reservation = Rezervace.objects.get(id=self.reservation.id)
        self.assertEqual(updated_reservation.stav, 2)

    def test_bad_request_method(self):
        """
        Tests that unsupported request method return right result
        """
        response = self.client.get(self.url, self.request)
        self.assertContains(response, 'error', status_code=200)

        response = self.client.delete(self.url, self.request)
        self.assertContains(response, 'error', status_code=200)

        response = self.client.put(self.url, self.request)
        self.assertContains(response, 'error', status_code=200)


class PayReservationTest(TestCase):
    def setUp(self):
        self.user = mommy.make(User)
        self.user.konto = 10000
        self.user.email = "user@user.cz"
        self.user.set_password('heslo')
        self.user.is_active = True
        self.user.save()

        self.reservation = mommy.make(Rezervace)
        self.reservation.zaplaceno = False
        self.reservation.cena = 200
        self.reservation.zakaznik = self.user
        self.reservation.save()

        self.admin = mommy.make(User)
        self.admin.is_superuser = True
        self.admin.is_active = True
        self.admin.email = "admin@admin.cz"
        self.admin.set_password('heslo')
        self.admin.save()

        self.client = Client()
        self.url = reverse('ajax-pay')

        self.request = {
            'rezervace_id': self.reservation.id,
        }

    def test_success_pay(self):
        res = self.client.login(email='admin@admin.cz', password='heslo')
        response = self.client.post(self.url, self.request)
        self.assertContains(response, "ok", status_code=200)

    def test_no_money(self):
        self.user.konto = 0
        self.user.save()

        res = self.client.login(email='admin@admin.cz', password='heslo')
        response = self.client.post(self.url, self.request)
        self.assertContains(response, "nomoney", status_code=200)

    def test_already_paid(self):
        self.reservation.zaplaceno = True
        self.reservation.save()

        res = self.client.login(email='admin@admin.cz', password='heslo')
        response = self.client.post(self.url, self.request)
        self.assertContains(response, "alreadypaid", status_code=200)

    def test_access_error(self):
        res = self.client.login(email='user@user.cz', password='heslo')
        response = self.client.post(self.url, self.request)
        self.assertContains(response, "accesserror", status_code=200)


class VoucheryViewTest(TestCase):
    def setUp(self):
        self.user = mommy.make(User)
        self.user.konto = 10000
        self.user.email = "user@user.cz"
        self.user.set_password('heslo')
        self.user.is_active = True
        self.user.save()

        self.voucher = mommy.make(Voucher)
        self.voucher.platny_od = datetime.datetime.now().replace(year=datetime.datetime.now().year - 1)
        self.voucher.platny_do = datetime.datetime.now().replace(year=datetime.datetime.now().year + 1)
        self.voucher.save()

        self.client = Client()

        self.url = reverse('web-vouchery')

    def test_get(self):
        """
        Tests that GET request work
        """
        res = self.client.login(email='user@user.cz', password='heslo')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_uplatnit_voucher(self):
        """
        Tests that take voucher benefit work
        """
        res = self.client.login(email='user@user.cz', password='heslo')
        response = self.client.post(self.url, {'id_voucher': self.voucher.id}, follow=True)
        self.assertContains(response, u"Voucher na částku", status_code=200)

    def test_uplatneny_voucher(self):
        """
        Tests that taken voucher work
        """
        voucher_upl = mommy.make(Voucher)
        voucher_upl.uplatnil_uzivatel = self.user
        voucher_upl.save()

        res = self.client.login(email='user@user.cz', password='heslo')
        response = self.client.post(self.url, {'id_voucher': voucher_upl.id}, follow=True)
        self.assertContains(response, u"Voucher již byl uplatněn", status_code=200)

    def test_neplatny_voucher(self):
        """
        Tests that voucher ot of date work
        """
        voucher = mommy.make(Voucher)
        voucher.platny_od = datetime.datetime.now().replace(year=datetime.datetime.now().year - 2)
        voucher.platny_do = datetime.datetime.now().replace(year=datetime.datetime.now().year - 1)
        voucher.save()

        res = self.client.login(email='user@user.cz', password='heslo')
        response = self.client.post(self.url, {'id_voucher': voucher.id}, follow=True)
        self.assertContains(response, u"Bohužel, platnost voucheru je od", status_code=200)

    def test_neexistujici_voucher(self):
        """
        Tests that non existing voucher work
        """
        res = self.client.login(email='user@user.cz', password='heslo')
        response = self.client.post(self.url, {'id_voucher': 2567663531}, follow=True)
        self.assertContains(response, u"Voucher neexistuje", status_code=200)

    def test_nezadany_voucher(self):
        """
        Tests that not included voucher work
        """

        res = self.client.login(email='user@user.cz', password='heslo')
        response = self.client.post(self.url, {}, follow=True)
        self.assertContains(response, u"Nebyl zadan voucher", status_code=200)





