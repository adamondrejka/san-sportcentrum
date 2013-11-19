# -*- coding: utf-8 -*-
# Create your views here.
from datetime import datetime
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils import timezone
from django.utils.timezone import utc
from core.models import Voucher, SportovniCentrum, Sportoviste


def home_view(request):
    return render(request, 'web/index.html')


def rezervace_view(request):
    sport_centers = SportovniCentrum.objects.all().order_by('nazev')
    return render(request, 'web/rezervace.html', {'sport_centers': sport_centers})


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
        id_voucher = request.POST.get('id_voucher')
        if id_voucher:
            try:
                voucher = Voucher.objects.get(id=id_voucher)

                date_now = timezone.now()

                if voucher.uplatnil_uzivatel:
                    messages.error(request, u"Voucher již byl uplatněn")
                    return redirect('web-vouchery')

                if voucher.platny_od < date_now < voucher.platny_do:
                    voucher.uplatnil_uzivatel = request.user
                    voucher.save()
                    request.user.add_money(voucher.castka)
                    messages.success(request, u"Voucher na částku {0} Kč byl úspěšně uplatněn".format(voucher.castka))

                else:
                    messages.error(request, u"Bohužel, platnost voucheru je od {0} do {1}".format(voucher.platny_od, voucher.platny_do))

                return redirect('web-vouchery')

            except Voucher.DoesNotExist:
                messages.error(request, u"Voucher neexistuje")
        else:
            messages.error(request, u"Nebyl zadan voucher")

        return redirect('web-vouchery')


@login_required()
def nastaveni_view(request):
    if request.method == "GET":
        return render(request, "web/nastaveni.html")
    elif request.method == "POST":
        action = request.POST.get("action_type")

        if action == "money_inc":
            # dobiti kreditu
            money = request.POST.get("amount_money")

            if money:
                request.user.add_money(float(money))
                messages.success(request, u"Kredit byl navýšen o částku {0} Kč".format(money))
            else:
                messages.error(request, u"Nepvoedlo se navýšit kredit")

        return redirect('web-vouchery')


def ajax_get_sportoviste(request):
    if request.method == "GET":
        sport_centrum = request.GET.get('id_sportovni_centrum')
        sportoviste = Sportoviste.objects.filter(sportovni_centrum_id=sport_centrum)



