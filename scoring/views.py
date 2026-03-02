from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from .models import (
    AgeGroup,
    Archer,
    Category,
    Club,
    Competition,
    Discipline,
    Round,
    Score,
    ScoringSheet,
    TargetFace,
    TargetFaceNameChoice,
    Team,
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

# AgeGroup

def agegroups(request):
    agegroups = AgeGroup.objects.all()
    template = 'scoring/django/agegroup/index.html'
    context = {'agegroups': agegroups}

    return render(request, template, context)

@login_required(login_url='scoring/my-login')
def create_agegroup(request):
    pass

# Archer

def archers(request):
    archers = Archer.objects.all()
    template = 'scoring/django/archer/index.html'
    context = {'archers': archers}

    return render(request, template, context)

# Category

def categories(request):
    categories = Category.objects.all()
    template = 'scoring/django/category/index.html'
    context = {'categories': categories}

    return render(request, template, context)

# Club

def clubs(request):
    clubs = Club.objects.all()
    template = 'scoring/django/club/index.html'
    context = {'clubs': clubs}

    return render(request, template, context)

# Competition

def competitions(request):
    competitions = Competition.objects.all()
    template = 'scoring/django/competition/index.html'
    context = {'competitions': competitions}

    return render(request, template, context)

# Discipline

def disciplines(request):
    disciplines = Discipline.objects.all()
    template = 'scoring/django/discipline/index.html'
    context = {'disciplines': disciplines}

    return render(request, template, context)

# Round

def rounds(request):
    rounds = Round.objects.all()
    template = 'scoring/django/round/index.html'
    context = {'rounds': rounds}

    return render(request, template, context)

# Score

def scores(request):
    scores = Score.objects.all()
    template = 'scoring/django/score/index.html'
    context = {'scores': scores}

    return render(request, template, context)

# ScoringSheet

def scoringsheets(request):
    scoringsheets = ScoringSheet.objects.all()
    template = 'scoring/django/scoringsheet/index.html'
    context = {'scoringsheets': scoringsheets}

    return render(request, template, context)

# TargetFace

def targetfaces(request):
    targetfaces = TargetFace.objects.all()
    template = 'scoring/django/targetface/index.html'
    context = {'targetfaces': targetfaces}

    return render(request, template, context)

# Team

def teams(request):
    teams = Team.objects.all()
    template = 'scoring/django/team/index.html'
    context = {'teams': teams}

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

@login_required(login_url='scoring/my-login')
def dashboard(request):
    return render(request, 'scoring/django/dashboard.html')

# - User logout

def user_logout(request):
    auth.logout(request)

    return redirect("scoring_my-login")