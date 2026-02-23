from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from .models import (
    Archer
)

from .forms import CreateUserForm, LoginForm

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

# Register a user

def register(request):
    form = CreateUserForm()
    
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            
            # return.redirect('')
    
    context = {'form': form}

    return render(request, 'scoring/django/register.html', context=context)

