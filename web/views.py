# Create your views here.
from django.shortcuts import render


def home_view(request):
    return render(request, 'web/index.html')


def rezervace_view(request):
    return render(request, 'web/rezervace.html')

def onas_view(request):
    return render(request, 'web/onas.html')

def kontakt_view(request):
    return render(request, 'web/kontakt.html')