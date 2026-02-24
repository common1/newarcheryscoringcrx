from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from .models import (
    Archer
)

from .forms import CreateUserForm, LoginForm

from django.contrib.auth.models import auth
from django.contrib.auth import authenticate

from django.contrib.auth.decorators import login_required

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
            
            return redirect('scoring_my-login')


    
    context = {'form': form}

    return render(request, 'scoring/django/register.html', context=context)

# - Login a user

def my_login(request):
    form = LoginForm()

    if request.method == "POST":
        form = LoginForm(request, data=request.POST)

        if form.is_valid():
            email = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, email=email, password=password)

            if user is not None:
                auth.login(request, user)

            return redirect('scoring_dashboard')

    context = {'form': form }

    return render(request, 'scoring/django/my-login.html', context=context)

# - Dashboard

@login_required(login_url='my-login')
def dashboard(request):
    return render(request, 'scoring/django/dashboard.html')

# - User logout

def user_logout(request):
    auth.logout(request)

    return redirect("scoring_my-login")