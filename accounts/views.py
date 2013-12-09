# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect, render
from django.views.generic import UpdateView
from accounts.forms import RegistrationForm, UzivatelForm
from accounts.utils import send_activation_email, make_activation_string, check_activation_string
from administration.views import StaffMemberRequiredMixin
from core.models import User


@login_required
def logout_view(request):
    logout(request)
    messages.success(request, u'Byl jste úspěšně odhlášen')
    return redirect('accounts-login')


def login_view(request):
    """
    View to log users in futruy
    Name in urls: "accounts_login"
    """
    full_path = request.get_full_path()

    if request.method == 'GET':
        return render(request, 'accounts/login.html', {
            'full_path': full_path,
        })

    elif request.method == 'POST':

        if request.POST['email'] != "" and request.POST['password'] != "":

            email = request.POST['email']
            password = request.POST['password']

            user = authenticate(email=email, password=password)

            if user:
                login(request, user)
                return redirect(request.GET.get('next', '/'))
            else:
                messages.error(request, u'Špatný email nebo heslo')

        else:
            messages.error(request, u"Musíte vyplnit e-mail a heslo")

        return render(request, 'accounts/login.html', {
            'full_path': full_path
        })


def registration_view(request):
    if request.method == 'GET':
        form = RegistrationForm()

        return render(request, 'accounts/registration.html', {'form': form})

    elif request.method == 'POST':

        form = RegistrationForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data['email']
            heslo = form.cleaned_data['heslo']
            jmeno = form.cleaned_data['jmeno']
            prijmeni = form.cleaned_data['prijmeni']
            rodne_cislo = form.cleaned_data['rodne_cislo']
            telefon = form.cleaned_data['telefon']

            #TODO: Add more user info

            # check if user already exists
            try:
                User.objects.get(email=email)
                messages.error(request, u'Uživatel již existuje')
                return render(request, 'accounts/registration.html', {'form': form})
            except User.DoesNotExist:
                user, password = User.objects.create_user(email, heslo)
                send_activation_email(user)
                user.jmeno = jmeno
                user.prijmeni = prijmeni
                user.rodne_cislo = rodne_cislo
                user.telefon = telefon
                user.save()

                return render(request, 'accounts/registration.html',
                              {
                                  'success': True
                              })
        else:
            return render(request, 'accounts/registration.html', {'form': form})


def activate_account_view(request):
    if request.method == 'GET':
        activation_string = request.REQUEST.get('as')
        user_id = request.REQUEST.get('ui')

        if activation_string and user_id:
            user = User.objects.get(id=user_id)

            test_string = make_activation_string(user)

            if not user.is_active and check_activation_string(user, test_string):
                user.activate()
                auth_user = authenticate(email=user.email, without_password=True)
                login(request, auth_user)
                messages.success(request, u'Účet byl úspěšně aktivován')
            else:
                messages.error(request, u'Účet již je aktivní nebo je aktivační odkaz nesprávný')
        else:
            messages.error(request, u'Účet již je aktivní nebo je aktivační odkaz nesprávný')

        return render(request, 'accounts/activation.html')


def detail_view(request):
    if request.method == "POST":
        form = UzivatelForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.info(request, u"Změny byly uloženy")
            return redirect(reverse_lazy('accounts-detail'))
        else:
            return render(request, 'accounts/detail.html', {'form': form})
    elif request.method == "GET":

        form = UzivatelForm(instance=request.user)
        return render(request, 'accounts/detail.html', {'form': form})

