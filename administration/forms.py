# -*- coding: utf-8 -*-
from django.forms import ModelForm,  widgets, forms
from django.forms.models import inlineformset_factory
from django import forms
from core.models import Voucher, Sportoviste, SportovisteMisto, User


class DateTimeInput(widgets.TextInput):
    """Subclass TextInput since there's no direct way to override its type attribute"""
    input_type = 'date'

    def __init__(self, *args, **kwargs):
        super(DateTimeInput, self).__init__(*args, **kwargs)


class VoucherForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(VoucherForm, self).__init__(*args, **kwargs)
        #self.fields['platny_od'].widget = DateTimeInput
        #self.fields['platny_do'].widget = DateTimeInput

    class Meta:
        model = Voucher


class SportovisteForm(ModelForm):
    class Meta:
        model = Sportoviste


class UzivatelForm(ModelForm):

    pass1 = forms.CharField(label=u"Heslo", required=False)

    class Meta:
        model = User
        fields = ['jmeno', 'prijmeni', 'email', 'RC', 'telefon','last_login', 'is_manager', 'is_superuser', 'is_active']

    def save(self, commit=True):
        user = super(UzivatelForm, self).save(commit=commit)
        heslo = self.cleaned_data['pass1']

        if heslo:
            user.set_password(heslo)
            if commit:
                user.save()

        return user

SportovisteMistoFormSet = inlineformset_factory(Sportoviste, SportovisteMisto, fields=('nazev', ), can_delete=True, extra=3)
