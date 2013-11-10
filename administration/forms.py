# -*- coding: utf-8 -*-
from django.forms import ModelForm,  widgets
from django.forms.models import inlineformset_factory
from core.models import Voucher, Sportoviste, SportovisteMisto


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

SportovisteMistoFormSet = inlineformset_factory(Sportoviste, SportovisteMisto, fields=('nazev', ), can_delete=True, extra=3)
