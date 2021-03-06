# -*- coding: utf-8 -*-
# Create your views here.
from functools import wraps
import random
from dateutil import parser
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy
from django.db import transaction
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from administration.forms import VoucherForm, SportovisteForm, SportovisteMistoFormSet, UzivatelForm
from core.models import Voucher, Sportoviste, SportovniCentrum, Rezervace, User


def staff_member_required2(view_func):
    """
    Decorator for views that checks that the user is logged in and is a staff
    member, displaying the login page if necessary.
    """
    @wraps(view_func)
    def _checklogin(request, *args, **kwargs):
        if request.user.is_active and request.user.is_staff:
            # The user is valid. Continue to the admin page.
            return view_func(request, *args, **kwargs)
        messages.error(request, u'Přístup povolen jen zaměstnancům')
        return redirect('accounts-login')
    return _checklogin

class StaffMemberRequiredMixin(object):
    """
    View mixin which requires that the user is authenticated.
    """
    @method_decorator(staff_member_required2)
    def dispatch(self, request, *args, **kwargs):
        return super(StaffMemberRequiredMixin, self).dispatch(request, *args, **kwargs)

@staff_member_required2
def home_view(request):
    return render(request, 'administration/index.html')


class VoucherList(StaffMemberRequiredMixin, ListView):
    model = Voucher
    paginate_by = 50
    queryset = Voucher.objects.all().order_by('-id')
    template_name = "administration/vouchers.html"
    context_object_name = 'vouchers'


class VoucherCreate(StaffMemberRequiredMixin, CreateView):
    model = Voucher
    template_name = 'administration/voucher_create.html'
    success_url = '/administration/voucher/add/'
    form_class = VoucherForm

    # Valid
    def form_valid(self, form):
        messages.success(self.request, u"Voucher byl úspěšně přidán")
        return super(VoucherCreate, self).form_valid(form)

    # Invalid
    def form_invalid(self, form):
        return super(VoucherCreate, self).form_invalid(form)


class VoucherUpdate(StaffMemberRequiredMixin, UpdateView):
    model = Voucher
    template_name = 'administration/voucher_create.html'
    success_url = '/administration/vouchery/'
    form_class = VoucherForm

    # Valid
    def form_valid(self, form):
        messages.success(self.request, u"Voucher byl úspěšně uložen")
        return super(VoucherUpdate, self).form_valid(form)

    # Invalid
    def form_invalid(self, form):
        return super(VoucherUpdate, self).form_invalid(form)


class VoucherDelete(StaffMemberRequiredMixin, DeleteView):
    model = Voucher
    success_url = reverse_lazy('admin-vouchery')
    template_name = 'administration/check_delete.html'

class SportovisteList(StaffMemberRequiredMixin, ListView):
    model = Sportoviste
    paginate_by = 50
    queryset = Sportoviste.objects.all().order_by('nazev')
    template_name = "administration/sportoviste_list.html"
    context_object_name = 'sportoviste'


class SportovisteCreate(StaffMemberRequiredMixin, CreateView):
    model = Sportoviste
    template_name = 'administration/sportoviste_create.html'
    success_url = reverse_lazy('admin-sportoviste-create')

    # Valid
    def form_valid(self, form):
        context = self.get_context_data()
        sportovistemisto_form = context['sportovistemisto_form']
        if sportovistemisto_form.is_valid():
            self.object = form.save()
            sportovistemisto_form.instance = self.object
            sportovistemisto_form.save()
            messages.success(self.request, u"Sportoviště bylo úspěšně přidáno")
        else:
            return self.render_to_response(self.get_context_data(form=form))

        return super(SportovisteCreate, self).form_valid(form)

    # Invalid
    def form_invalid(self, form):
        return super(SportovisteCreate, self).form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super(SportovisteCreate, self).get_context_data(**kwargs)
        if self.request.POST:
            context['sportovistemisto_form'] = SportovisteMistoFormSet(self.request.POST)
        else:
            context['sportovistemisto_form'] = SportovisteMistoFormSet()
        return context


class SportovisteUpdate(StaffMemberRequiredMixin, UpdateView):
    model = Sportoviste
    template_name = 'administration/sportoviste_create.html'
    success_url = '/administration/sportoviste/'

    # Valid
    def form_valid(self, form):
        context = self.get_context_data()
        sportovistemisto_form = context['sportovistemisto_form']
        if sportovistemisto_form.is_valid():
            self.object = form.save()
            sportovistemisto_form.instance = self.object
            sportovistemisto_form.save()
            messages.success(self.request, u"Sportoviště byl úspěšně uložen")
        else:
            return self.render_to_response(self.get_context_data(form=form))

        return super(SportovisteUpdate, self).form_valid(form)

    # Invalid
    def form_invalid(self, form):
        return super(SportovisteUpdate, self).form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super(SportovisteUpdate, self).get_context_data(**kwargs)
        if self.request.POST:
            context['sportovistemisto_form'] = SportovisteMistoFormSet(self.request.POST, instance=self.object)
        else:
            context['sportovistemisto_form'] = SportovisteMistoFormSet(instance=self.object)
        return context


class SportovisteDelete(StaffMemberRequiredMixin, DeleteView):
    model = Sportoviste
    success_url = reverse_lazy('admin-sportoviste')
    template_name = 'administration/check_delete.html'


class SportovniCentrumList(StaffMemberRequiredMixin, ListView):
    model = SportovniCentrum
    paginate_by = 50
    queryset = SportovniCentrum.objects.all().order_by('-id')
    template_name = "administration/sportovnicentrum_list.html"
    context_object_name = 'sportovnicentra'


class SportovniCentrumCreate(StaffMemberRequiredMixin, CreateView):
    model = SportovniCentrum
    template_name = 'administration/sportovnicentrum_create.html'
    success_url = reverse_lazy('admin-sportovnicentrum-create')

    # Valid
    def form_valid(self, form):
        messages.success(self.request, u"Sportovní centrum bylo úspěšně přidáno")
        return super(SportovniCentrumCreate, self).form_valid(form)

    # Invalid
    def form_invalid(self, form):
        return super(SportovniCentrumCreate, self).form_invalid(form)


class SportovniCentrumUpdate(StaffMemberRequiredMixin, UpdateView):
    model = SportovniCentrum
    template_name = 'administration/sportovnicentrum_create.html'
    success_url = reverse_lazy('admin-sportovnicentra')

    # Valid
    def form_valid(self, form):
        messages.success(self.request, u"Sportovní centrum bylo úspěšně uloženo")
        return super(SportovniCentrumUpdate, self).form_valid(form)

    # Invalid
    def form_invalid(self, form):
        return super(SportovniCentrumUpdate, self).form_invalid(form)


class SportovniCentrumDelete(StaffMemberRequiredMixin, DeleteView):
    model = SportovniCentrum
    success_url = reverse_lazy('admin-sportovnicentra')
    template_name = 'administration/check_delete.html'


class RezervaceList(StaffMemberRequiredMixin, ListView):
    model = Rezervace
    paginate_by = 50
    queryset = Rezervace.objects.all().order_by('-id')
    template_name = "administration/rezervace_list.html"
    context_object_name = 'rezervace'


class RezervaceDetail(StaffMemberRequiredMixin, DetailView):
    model = Rezervace
    template_name = 'administration/rezervace_detail.html'


class RezervaceDelete(StaffMemberRequiredMixin, DeleteView):
    model = Rezervace
    success_url = reverse_lazy('admin-rezervace')
    template_name = 'administration/check_delete.html'


class UzivatelList(StaffMemberRequiredMixin, ListView):
    model = User
    paginate_by = 50
    queryset = User.objects.all().order_by('email')
    template_name = "administration/uzivatel_list.html"
    context_object_name = 'uzivatele'


class UzivatelCreate(StaffMemberRequiredMixin, CreateView):
    model = User
    template_name = 'administration/uzivatel_create.html'
    success_url = reverse_lazy('admin-uzivatel-create')
    form_class = UzivatelForm

    # Valid
    def form_valid(self, form):
        messages.success(self.request, u"Uživatel byl úspěšně přidán")
        return super(UzivatelCreate, self).form_valid(form)

    # Invalid
    def form_invalid(self, form):
        return super(UzivatelCreate, self).form_invalid(form)


class UzivatelUpdate(StaffMemberRequiredMixin, UpdateView):
    model = User
    template_name = 'administration/uzivatel_create.html'
    success_url = reverse_lazy('admin-uzivatele')
    form_class = UzivatelForm

    # Valid
    def form_valid(self, form):
        messages.success(self.request, u"Uživatel bylo úspěšně uložen")
        return super(UzivatelUpdate, self).form_valid(form)

    # Invalid
    def form_invalid(self, form):
        return super(UzivatelUpdate, self).form_invalid(form)


class UzivatelDelete(StaffMemberRequiredMixin, DeleteView):
    model = User
    success_url = reverse_lazy('admin-uzivatele')
    template_name = 'administration/check_delete.html'


def generate_vouchers(request):

    def random_code():
        return random.randint(10000000, 99999999999)

    if request.method == "POST":
        count = int(request.POST.get('voucher_count', 0))
        platnost_od = request.POST.get('platnost_od')
        platnost_do = request.POST.get('platnost_do')
        castka = float(request.POST.get('castka', 0))
        user = request.user

        if count and platnost_do and platnost_od and castka:
            with transaction.atomic():
                for i in xrange(0, count):
                    v = Voucher()
                    v.castka = castka
                    v.vydal_uzivatel = user
                    v.platny_od = parser.parse(platnost_od)
                    v.platny_do = parser.parse(platnost_do)
                    v.id = random_code()
                    v.save()

                messages.success(request, u"Úspěšně vygenerováno")

        else:
            messages.info(request, u"Nevygenerováno, musíte zadat všechny hodnoty")

        return redirect('admin-vouchery')

