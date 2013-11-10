# -*- coding: utf-8 -*-
from django import forms

__author__ = 'adam'


class RegistrationForm(forms.Form):
    """
    Form for creating new user
    """

    jmeno = forms.CharField(label=u"Jméno")
    prijmeni = forms.CharField(label=u"Příjmení")
    rodne_cislo = forms.CharField(label=u"Rodné číslo")
    heslo = forms.CharField(widget=forms.PasswordInput, label=u"Heslo")
    heslo2 = forms.CharField(widget=forms.PasswordInput, label=u"Heslo znovu")
    telefon = forms.CharField(label=u"Telefón")
    email = forms.EmailField(label=u"Email")

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        heslo = cleaned_data.get("heslo")
        heslo2 = cleaned_data.get("heslo2")

        if heslo != heslo2:
            del cleaned_data['heslo']
            del cleaned_data['heslo2']

            raise forms.ValidationError(u"Hesla se neshodují")
        else:
            return cleaned_data