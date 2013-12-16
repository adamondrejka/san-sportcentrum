# -*- coding: utf-8 -*-
# Create your views here.
from datetime import datetime
import json
from dateutil import parser
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils import timezone
from django.utils.timezone import utc
from core.models import Voucher, SportovniCentrum, Sportoviste, User, Rezervace, SportovisteMisto


def home_view(request):
    sportovni_centra = SportovniCentrum.objects.all().order_by('nazev')
    return render(request, 'web/index.html', {'sportovni_centra': sportovni_centra})


def rezervace_view(request):
    sport_centers = SportovniCentrum.objects.all().order_by('nazev')
    users = User.objects.all().order_by('prijmeni') if request.user.is_superuser else []
    states = Rezervace.STAV_CHOICES
    my_reservations = Rezervace.objects.filter(zakaznik_id=request.user.id, rezervace_od__gte=datetime.now(), stav=0) if request.user else []
    return render(request, 'web/rezervace.html', {'sport_centers': sport_centers, 'users': users, 'states': states,
                                                  'my_reservations': my_reservations})


def onas_view(request):
    return render(request, 'web/onas.html')


def kontakt_view(request):
    return render(request, 'web/kontakt.html')


@login_required
def vouchery_view(request):
    if request.method == "GET":
        vouchers = Voucher.objects.filter(uplatnil_uzivatel=request.user)
        return render(request, 'web/vouchery.html', {'vouchers': vouchers})
    elif request.method == "POST":
        try:
            id_voucher = request.POST.get('id_voucher')
            if id_voucher:
                voucher = Voucher.objects.get(id=id_voucher)

                date_now = timezone.now()

                if voucher.uplatnil_uzivatel:
                    messages.error(request, u"Voucher již byl uplatněn")

                elif voucher.platny_od < date_now < voucher.platny_do:
                    voucher.uplatnil_uzivatel = request.user
                    voucher.save()
                    request.user.add_money(voucher.castka)
                    messages.success(request, u"Voucher na částku {0} Kč byl úspěšně uplatněn".format(voucher.castka))

                else:
                    messages.error(request, u"Bohužel, platnost voucheru je od {0} do {1}".format(voucher.platny_od, voucher.platny_do))

            else:
                messages.error(request, u"Nebyl zadan voucher")
        except Exception:
            messages.error(request, u"Voucher neexistuje")

        return redirect('web-vouchery')


@login_required()
def kredit_view(request):
    if request.method == "GET":
        return render(request, "web/kredit.html")
    elif request.method == "POST":
        try:
            action = request.POST.get("action_type")

            if action == "money_inc":
                # dobiti kreditu
                money = request.POST.get("amount_money")

                if money:
                    request.user.add_money(float(money))
                    messages.success(request, u"Kredit byl navýšen o částku {0} Kč".format(money))
                else:
                    messages.error(request, u"Nepvoedlo se navýšit kredit")
        except Exception:
            messages.error(request, u"Nepodařilo se navýšit kredit")

        return redirect('web-kredit')

@login_required
def cancel_reservation(request):
    if request.method == "GET":
        try:
            id_rezervace = request.GET.get('id_rezervace')
            rezervace = Rezervace.objects.get(id=id_rezervace)

            date_now = timezone.now()
            date = date_now.replace(hour=date_now.hour-5)

            if rezervace.rezervace_od < date and (rezervace.zakaznik == request.user or request.user.is_staff):
                rezervace.delete()
                messages.success(request, u"Úspěšně zrušeno")
            else:
                messages.error(request, u"Nepodařilo se zrušit rezervaci, je po termínu nebo nemáte oprvánění")
        except Exception, e:
            messages.error(request, u"Nepodařilo se zrušit rezervaci")

        return redirect('rezervace')


def ajax_get_sportoviste(request):
    if request.method == "GET":
        sport_centrum = request.GET.get('id_sportovni_centrum')
        sportoviste = Sportoviste.objects.filter(sportovni_centrum_id=sport_centrum).order_by('nazev')

        result = {'result': [s.serialize() for s in sportoviste]}
        return HttpResponse(json.dumps(result), content_type="application/json")


def ajax_get_table_calendar(request):
    if request.method == "GET":
        sportoviste_id = request.GET.get('id_sportoviste')
        datum = request.GET.get('datum')
        datum = parser.parse(datum)

        sportoviste = Sportoviste.objects.get(id=sportoviste_id)
        mista = sportoviste.sportovistemisto_set.all().order_by('nazev')
        result_sportoviste = sportoviste.serialize()
        result_mista = [m.serialize(datum) for m in mista]

        # oznac uzivatelovi jeho rezervace
        if not request.user.is_staff:
            for m in result_mista:
                for r in m['rezervace']:
                    is_my = False
                    if r['zakaznik_id'] == request.user.id:
                        is_my = True
                    r['is_my'] = is_my

        result = {
            'result_sportoviste': result_sportoviste,
            'result_mista': result_mista
        }
    else:
        result = {
            'status': 'error'
        }

    return HttpResponse(json.dumps(result), content_type="application/json")


def ajax_make_reservation(request):

    def get_hours_and_minutes(minutes):
        return minutes / 60, minutes % 60

    if request.method == "POST":
        zakaznik = request.REQUEST.get('zakaznik', request.user.id)
        misto = request.REQUEST.get('sportoviste_misto')
        datum = request.REQUEST.get('rezervace_datum')
        rezervace_od = request.REQUEST.get('rezervace_od')
        rezervace_do = request.REQUEST.get('rezervace_do')
        stav = request.REQUEST.get('stav', 0)
        rezervace_id = request.REQUEST.get('rezervace_id')

        if rezervace_id:
            rezervace = Rezervace.objects.get(id=rezervace_id)
        else:
            rezervace = Rezervace()

        user = User.objects.get(id=zakaznik)
        sport_misto = SportovisteMisto.objects.get(id=misto)
        sportoviste = sport_misto.sportoviste

        cena = ((int(rezervace_do) - int(rezervace_od)) / sportoviste.interval_vypujcek_minuty()) * sportoviste.cena_interval

        if user.konto < cena and stav == 0 and not request.user.is_staff:
            result = {'result': 'nomoney'}

        else:
            rezervace.zakaznik_id = zakaznik
            rezervace.misto_id = misto
            od_hodiny, od_minuty = get_hours_and_minutes(int(rezervace_od))
            do_hodiny, do_minuty = get_hours_and_minutes(int(rezervace_do))
            datum_od = parser.parse(datum).replace(hour=od_hodiny, minute=od_minuty)
            datum_do = parser.parse(datum).replace(hour=do_hodiny, minute=do_minuty)

            with transaction.atomic():
                rezervace.rezervace_od = datum_od
                rezervace.rezervace_do = datum_do
                rezervace.stav = stav
                rezervace.cena = cena
                rezervace.zaplaceno = True
                rezervace.save()

                user.konto -= cena
                user.save()

            result = {'result': 'ok'}

    else:
        result = {'result': 'error'}

    return HttpResponse(json.dumps(result), content_type="application/json")


def ajax_pay(request):
    rezervace_id = request.REQUEST.get('rezervace_id')
    rezervace = Rezervace.objects.get(id=rezervace_id)
    zakaznik = rezervace.zakaznik

    if request.user.is_staff:
        if rezervace.zaplaceno:
            rezervace.stav = 2
            rezervace.save()
            result = {'result': 'alreadypaid'}

        elif not rezervace.zaplaceno and zakaznik.konto >= rezervace.cena:
            rezervace.stav = 2
            rezervace.zaplaceno = True
            rezervace.save()

            zakaznik.konto -= rezervace.cena
            zakaznik.save()

            result = {'result': 'ok'}
        else:
            result = {'result': 'nomoney'}
    else:
        result = {'result': 'accesserror'}

    return HttpResponse(json.dumps(result), content_type="application/json")


def ajax_delete_rezervace(request):
    rezervace_id = request.REQUEST.get('rezervace_id')
    with transaction.atomic():
        rezervace = Rezervace.objects.get(id=rezervace_id)
        if rezervace.zaplaceno:
            request.user.konto += rezervace.cena
            request.user.save()

        rezervace.delete()
    return HttpResponse(json.dumps({'result': 'ok'}), content_type="application/json")


