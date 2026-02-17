from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import (
    Archer
)

def scoring(request):
    template = 'scoring/django/scoring.html'

    return render(request, template)

def archers(request):
    archers = Archer.objects.all()
    template = 'scoring/django/archer/archers.html'
    context = {'archers': archers}

    return render(request, template, context)
