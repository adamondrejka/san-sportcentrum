# -*- coding: utf-8 -*-
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    jmeno = models.CharField(max_length=40, null=True)
    prijmeni = models.CharField(max_length=40, null=True)

    email = models.EmailField(db_index=True, unique=True, verbose_name=u"Email")
    RC = models.CharField(max_length=12)
    telefon = models.CharField(max_length=25)

    konto = models.FloatField(default=0, verbose_name=u"Konto")

    is_active = models.BooleanField(default=False, verbose_name=u"Aktivován")
    is_manager = models.BooleanField(default=False, verbose_name=u"Zaměstnanec")

    def get_full_name(self):
        return "{0} {1}".format(self.jmeno, self.prijmeni) if self.jmeno and self.prijmeni else self.email

    def get_short_name(self):
        return self.get_full_name()

    def activate(self):
        """ Activates user to using account on Futruy
        """
        self.is_active = True
        self.save()

    @property
    def is_staff(self):
        return self.is_manager or self.is_superuser

    USERNAME_FIELD = 'email'

    objects = UserManager()

    class Meta:
        db_table = 'users'

    def create_user(self, email, password, firstName=None, lastName=None, is_superuser=False, is_active=False, is_manager=False):

        self.email = email
        self.set_password(password)
        self.is_active = is_active
        self.is_superuser = is_superuser
        self.is_manager = is_manager
        self.first_name = firstName
        self.last_name = lastName
        self.set_activation_string()

        return self.save()

    def add_money(self, money_amount):
        """ Prida penize na konto uzivatele
        """
        self.konto += money_amount
        self.save()


class Voucher(models.Model):
    """
    """
    id = models.IntegerField(primary_key=True, verbose_name=u"ID voucheru")
    castka = models.FloatField(verbose_name=u"Částka")
    platny_od = models.DateTimeField(verbose_name=u"Platný od", help_text=u"ve tvaru yyyy-mm-dd")
    platny_do = models.DateTimeField(verbose_name=u"Platný do", help_text=u"ve tvaru yyyy-mm-dd")
    vydal_uzivatel = models.ForeignKey(User, verbose_name=u"Vydal uživatel")
    uplatnil_uzivatel = models.ForeignKey(User, null=True, blank=True, verbose_name=u"Uplatnil uživatel",
                                          related_name="uplatnil_uzivatel_set")

    def __unicode__(self):
        return "Voucher {0}".format(self.pk)


class SportovniCentrum(models.Model):
    """

    """
    nazev = models.CharField(max_length=50, verbose_name=u"Název")
    ulice = models.CharField(max_length=50, verbose_name=u"Ulice", help_text=u"Včetně čísla popisného a orientačního")
    mesto = models.CharField(max_length=50, verbose_name=u"Město")
    psc = models.IntegerField(max_length=5)
    popis = models.TextField(null=True, blank=True, verbose_name=u"Popis")

    def __unicode__(self):
        return u"{} {}".format(self.nazev, self.mesto)

    def adresa(self):
        return u"{} {}".format(self.ulice, self.mesto)


class Sportoviste(models.Model):
    sportovni_centrum = models.ForeignKey(SportovniCentrum, verbose_name=u"Sportovní centrum")
    nazev = models.CharField(max_length=60, verbose_name=u"Název")
    interval_vypujcek = models.TimeField(verbose_name=u"Interval výpujček", help_text=u"Ve formátu hh:mm (např. 1:30)")
    zacatek_provozu = models.TimeField(verbose_name=u"Začátek provozu", help_text=u"Ve formátu hh:mm (např. 9:30)")
    konec_provozu = models.TimeField(verbose_name=u"Konec provozu", help_text=u"Ve formátu hh:mm (např. 19:30)")
    cena_interval = models.FloatField(verbose_name=u"Cena za interval", help_text=u"V Kč")
    popis = models.TextField(null=True, blank=True, verbose_name=u"Popis")

    def __unicode__(self):
        return self.nazev

    def serialize(self):
        return {
            'nazev': self.nazev,
            'interval_vypujcek_hodiny': self.interval_vypujcek.hour,
            'interval_vypujcek_minuty': self.interval_vypujcek.minute,
            'interval_vypujcek': self.interval_vypujcek.minute + self.interval_vypujcek.hour * 60,
            'zacatek_provozu_hodiny': self.zacatek_provozu.hour,
            'zacatek_provozu_minuty': self.zacatek_provozu.minute,
            'zacatek_provozu': self.zacatek_provozu.minute + self.zacatek_provozu.hour * 60,
            'konec_provozu_hodiny': self.konec_provozu.hour,
            'konec_provozu_minuty': self.konec_provozu.minute,
            'konec_provozu': self.konec_provozu.minute + self.konec_provozu.hour * 60,
            'popis': self.popis,
            'cena_interval': self.cena_interval,
            'id': self.id
        }

    def interval_vypujcek_minuty(self):
        return self.interval_vypujcek.minute + self.interval_vypujcek.hour * 60


class SportovisteMisto(models.Model):
    """ Pridana trida, neni v analyze. Urcuje misto sportoviste (napr. Kurt 1, Kurt 2,
    Bowlingova draha 1, Bowlingova draha 2... )
    """

    sportoviste = models.ForeignKey(Sportoviste, verbose_name=u"Sportoviště")
    nazev = models.CharField(max_length=60, verbose_name=u"Název")

    def __unicode__(self):
        return u"{0} - {1} - {2}".format(self.sportoviste.sportovni_centrum.nazev, self.sportoviste.nazev, self.nazev)

    def serialize(self, date=None):
        date1 = date.replace(hour=0, minute=0) if date else None
        date2 = date.replace(hour=23, minute=59) if date else None

        rezervace_list = self.rezervace_set.all().order_by('rezervace_od') if not date else self.rezervace_set.filter(rezervace_od__gte=date1, rezervace_do__lte=date2).order_by('rezervace_od')

        return {
            'id': self.id,
            'nazev': self.nazev,
            'rezervace': [rezervace.serialize() for rezervace in rezervace_list]

        }


class Rezervace(models.Model):

    STAV_CHOICES = (
        (0, 'Rezervováno'),
        (1, 'Provozuje'),
        (2, 'Zaplacano'),
        (3, 'Propadlo'),
    )

    misto = models.ForeignKey(SportovisteMisto, verbose_name=u"Místo")
    zakaznik = models.ForeignKey(User, verbose_name=u"Zákazník")
    cena = models.FloatField(verbose_name=u"Cena")
    rezervace_od = models.DateTimeField(verbose_name=u"Rezervace od")
    rezervace_do = models.DateTimeField(verbose_name=u"Rezervace do")
    stav = models.SmallIntegerField(choices=STAV_CHOICES)
    # je rezervace jiz zaplacena?
    zaplaceno = models.BooleanField(default=False)

    def __unicode__(self):
        return u"{0} - {1} - {2}".format(self.misto.sportoviste, self.misto.nazev, self.zakaznik.get_full_name())

    def print_user(self):
        return u"{0} - {1} - {2}".format(self.misto.sportoviste, self.misto, self.rezervace_od)

    def serialize(self):
        return {
            'id': self.id,
            'zakaznik_id': self.zakaznik_id,
            'zakaznik_jmeno': self.zakaznik.get_full_name(),
            'rezervace_od': self.rezervace_od.isoformat(),
            'rezervace_od_alt': self.rezervace_od.minute + self.rezervace_od.hour * 60 + 60,
            'rezervace_do': self.rezervace_do.isoformat(),
            'rezervace_do_alt': self.rezervace_do.minute + self.rezervace_do.hour * 60 + 60,
            'rezervace_datum': self.rezervace_od.strftime("%m/%d/%Y"),
            'cena': self.cena,
            'stav': self.stav,
            'zaplaceno': self.zaplaceno
        }



