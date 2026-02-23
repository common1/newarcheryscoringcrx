from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import (
    Archer
)

def scoring(request):
    template = 'scoring/django/index.html'

    return render(request, template)

def database_tables(request):
    template = 'scoring/django/database_tables.html'

    return render(request, template)

def archers(request):
    archers = Archer.objects.all()
    template = 'scoring/django/archer/index.html'
    context = {'archers': archers}

    return render(request, template, context)
