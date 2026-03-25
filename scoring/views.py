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

    ScoringWizard,
)

from .forms import (
    CreateAgeGroupForm,
    UpdateAgeGroupForm,
    CreateArcherForm,
    UpdateArcherForm,
    UpdateCategoryForm,
    CreateCategoryForm,
    CreateClubForm,
    UpdateClubForm,
    CreateCompetitionForm,
    UpdateCompetitionForm,
    CreateDisciplineForm,
    UpdateDisciplineForm,
    CreateRoundForm,
    UpdateRoundForm,
    CreateScoreForm,
    UpdateScoreForm,
    CreateScoringSheetForm,
    UpdateScoringSheetForm,
    CreateTargetFaceForm,
    UpdateTargetFaceForm,
    CreateTeamForm,
    UpdateTeamForm,

    CreateUserForm,
    LoginForm,
    
    ScoringWizardForm,
)

from django.contrib.auth.models import auth
from django.contrib.auth import authenticate

from django.contrib.auth.decorators import login_required
from django.contrib import messages

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
    form = CreateAgeGroupForm()
    if request.method == "POST":
        form = CreateAgeGroupForm(request.POST)

        if form.is_valid():
            form.save()
            
            messages.success(request, "Age Group created successfully!")

            return redirect("scoring_agegroups")

    context = {'form': form}

    return render(request, 'scoring/django/agegroup/create.html', context=context)

@login_required(login_url='scoring/my-login')
def update_agegroup(request, pk):
    agegroup = AgeGroup.objects.get(id=pk)
    form = UpdateAgeGroupForm(instance=agegroup)

    if request.method == "POST":
        form = UpdateAgeGroupForm(request.POST, instance=agegroup)

        if form.is_valid():
            form.save()
            
            messages.success(request, "Age Group updated successfully!")

            return redirect("scoring_agegroups")

    context = {'form': form}

    return render(request, 'scoring/django/agegroup/update.html', context=context)

@login_required(login_url='scoring/my-login')
def singular_agegroup(request, pk):
    agegroup = AgeGroup.objects.get(id=pk)
    context = {'agegroup': agegroup}

    return render(request, 'scoring/django/agegroup/view.html', context)

@login_required(login_url='scoring/my-login')
def delete_agegroup(request, pk):
    agegroup = AgeGroup.objects.get(id=pk)
    agegroup.delete()

    messages.success(request, "Age Group deleted successfully!")

    return redirect("scoring_agegroups")

# Archer

def archers(request):
    archers = Archer.objects.all()
    template = 'scoring/django/archer/index.html'
    context = {'archers': archers}

    return render(request, template, context)

@login_required(login_url='scoring/my-login')
def create_archer(request):
    form = CreateArcherForm()
    if request.method == "POST":
        form = CreateArcherForm(request.POST)

        if form.is_valid():
            form.save()
            
            messages.success(request, "Archer created successfully!")

            return redirect("scoring_archers")

    context = {'form': form}

    return render(request, 'scoring/django/archer/create.html', context=context)

@login_required(login_url='scoring/my-login')
def update_archer(request, pk):
    archer = Archer.objects.get(id=pk)
    form = UpdateArcherForm(instance=archer)

    if request.method == "POST":
        form = UpdateArcherForm(request.POST, instance=archer)

        if form.is_valid():
            form.save()

            messages.success(request, "Archer updated successfully!")

            return redirect("scoring_archers")

    context = {'form': form}

    return render(request, 'scoring/django/archer/update.html', context=context)

@login_required(login_url='scoring/my-login')
def singular_archer(request, pk):
    archer = Archer.objects.get(id=pk)
    context = {'archer': archer}

    return render(request, 'scoring/django/archer/view.html', context)

@login_required(login_url='scoring/my-login')
def delete_archer(request, pk):
    archer = Archer.objects.get(id=pk)
    archer.delete()

    messages.success(request, "Archer deleted successfully!")

    return redirect("scoring_archers")

# Category

def categories(request):
    categories = Category.objects.all()
    template = 'scoring/django/category/index.html'
    context = {'categories': categories}

    return render(request, template, context)

@login_required(login_url='scoring/my-login')
def create_category(request):
    form = CreateCategoryForm()
    if request.method == "POST":
        form = CreateCategoryForm(request.POST)

        if form.is_valid():
            form.save()
            
            messages.success(request, "Category created successfully!")

            return redirect("scoring_categories")

    context = {'form': form}

    return render(request, 'scoring/django/category/create.html', context=context)

@login_required(login_url='scoring/my-login')
def update_category(request, pk):
    category = Category.objects.get(id=pk)
    form = UpdateCategoryForm(instance=category)

    if request.method == "POST":
        form = UpdateCategoryForm(request.POST, instance=category)

        if form.is_valid():
            form.save()
            
            messages.success(request, "Category updated successfully!")

            return redirect("scoring_categories")

    context = {'form': form}

    return render(request, 'scoring/django/category/update.html', context=context)

@login_required(login_url='scoring/my-login')
def singular_category(request, pk):
    category = Category.objects.get(id=pk)
    context = {'category': category}

    return render(request, 'scoring/django/category/view.html', context)

@login_required(login_url='scoring/my-login')
def delete_category(request, pk):
    category = Category.objects.get(id=pk)
    category.delete()

    messages.success(request, "Category deleted successfully!")

    return redirect("scoring_categories")

# Club

def clubs(request):
    clubs = Club.objects.all()
    template = 'scoring/django/club/index.html'
    context = {'clubs': clubs}

    return render(request, template, context)

@login_required(login_url='scoring/my-login')
def create_club(request):
    form = CreateClubForm()
    if request.method == "POST":
        form = CreateClubForm(request.POST)

        if form.is_valid():
            form.save()
            
            messages.success(request, "Club created successfully!")

            return redirect("scoring_clubs")

    context = {'form': form} 

    return render(request, 'scoring/django/club/create.html', context=context)

@login_required(login_url='scoring/my-login')
def update_club(request, pk):
    club = Club.objects.get(id=pk)
    form = UpdateClubForm(instance=club)

    if request.method == "POST":
        form = UpdateClubForm(request.POST, instance=club)

        if form.is_valid():
            form.save()

            messages.success(request, "Club updated successfully!")

            return redirect("scoring_clubs")

    context = {'form': form}

    return render(request, 'scoring/django/club/update.html', context=context)

@login_required(login_url='scoring/my-login')
def singular_club(request, pk):
    club = Club.objects.get(id=pk)
    context = {'club': club}

    return render(request, 'scoring/django/club/view.html', context)

@login_required(login_url='scoring/my-login')
def delete_club(request, pk):
    club = Club.objects.get(id=pk)
    club.delete()

    messages.success(request, "Club deleted successfully!")

    return redirect("scoring_clubs")

# Competition

def competitions(request):
    competitions = Competition.objects.all()
    template = 'scoring/django/competition/index.html'
    context = {'competitions': competitions}

    return render(request, template, context)

@login_required(login_url='scoring/my-login')
def create_competition(request):
    form = CreateCompetitionForm()
    if request.method == "POST":
        form = CreateCompetitionForm(request.POST)

        if form.is_valid():
            form.save()
            
            messages.success(request, "Competition created successfully!")

            return redirect("scoring_competitions")

    context = {'form': form}

    return render(request, 'scoring/django/competition/create.html', context=context)

@login_required(login_url='scoring/my-login')
def update_competition(request, pk):
    competition = Competition.objects.get(id=pk)
    form = UpdateCompetitionForm(instance=competition)

    if request.method == "POST":
        form = UpdateCompetitionForm(request.POST, instance=competition)

        if form.is_valid():
            form.save()
            
            messages.success(request, "Competition updated successfully!")

            return redirect("scoring_competitions")

    context = {'form': form}

    return render(request, 'scoring/django/competition/update.html', context=context)

@login_required(login_url='scoring/my-login')
def singular_competition(request, pk):
    competition = Competition.objects.get(id=pk)
    context = {'competition': competition}

    return render(request, 'scoring/django/competition/view.html', context)

@login_required(login_url='scoring/my-login')
def delete_competition(request, pk):
    competition = Competition.objects.get(id=pk)
    competition.delete()

    messages.success(request, "Competition deleted successfully!")

    return redirect("scoring_competitions")

# Discipline

def disciplines(request):
    disciplines = Discipline.objects.all()
    template = 'scoring/django/discipline/index.html'
    context = {'disciplines': disciplines}

    return render(request, template, context)

@login_required(login_url='scoring/my-login')
def create_discipline(request):
    form = CreateDisciplineForm()
    if request.method == "POST":
        form = CreateDisciplineForm(request.POST)

        if form.is_valid():
            form.save()
            
            messages.success(request, "Discipline created successfully!")

            return redirect("scoring_disciplines")

    context = {'form': form}

    return render(request, 'scoring/django/discipline/create.html', context=context)

@login_required(login_url='scoring/my-login')
def update_discipline(request, pk):
    discipline = Discipline.objects.get(id=pk)
    form = UpdateDisciplineForm(instance=discipline)

    if request.method == "POST":
        form = UpdateDisciplineForm(request.POST, instance=discipline)

        if form.is_valid():
            form.save()
            
            messages.success(request, "Discipline updated successfully!")

            return redirect("scoring_disciplines")

    context = {'form': form}

    return render(request, 'scoring/django/discipline/update.html', context=context)

@login_required(login_url='scoring/my-login')
def singular_discipline(request, pk):
    discipline = Discipline.objects.get(id=pk)
    context = {'discipline': discipline}

    return render(request, 'scoring/django/discipline/view.html', context)

@login_required(login_url='scoring/my-login')
def delete_discipline(request, pk):
    discipline = Discipline.objects.get(id=pk)
    discipline.delete()

    messages.success(request, "Discipline Deleted successfully!")

    return redirect("scoring_disciplines")

# Round

def rounds(request):
    rounds = Round.objects.all()
    template = 'scoring/django/round/index.html'
    context = {'rounds': rounds}

    return render(request, template, context)

@login_required(login_url='scoring/my-login')
def create_round(request):
    form = CreateRoundForm()
    if request.method == "POST":
        form = CreateRoundForm(request.POST)

        if form.is_valid():
            form.save()

            messages.success(request, "Round created successfully!")

            return redirect("scoring_rounds")

    context = {'form': form}

    return render(request, 'scoring/django/round/create.html', context=context)

@login_required(login_url='scoring/my-login')
def update_round(request, pk):
    round = Round.objects.get(id=pk)
    form = UpdateRoundForm(instance=round)

    if request.method == "POST":
        form = UpdateRoundForm(request.POST, instance=round)

        if form.is_valid():
            form.save()
            
            messages.success(request, "Round updated successfully!")

            return redirect("scoring_rounds")

    context = {'form': form}

    return render(request, 'scoring/django/round/update.html', context=context)

@login_required(login_url='scoring/my-login')
def singular_round(request, pk):
    round = Round.objects.get(id=pk)
    context = {'round': round}

    return render(request, 'scoring/django/round/view.html', context)

@login_required(login_url='scoring/my-login')
def delete_round(request, pk):
    round = Round.objects.get(id=pk)
    round.delete()

    messages.success(request, "Round deleted successfully!")

    return redirect("scoring_rounds")

# Score

def scores(request):
    scores = Score.objects.all()
    template = 'scoring/django/score/index.html'
    context = {'scores': scores}

    return render(request, template, context)

@login_required(login_url='scoring/my-login')
def create_score(request):
    form = CreateScoreForm()
    if request.method == "POST":
        form = CreateScoreForm(request.POST)

        if form.is_valid():
            form.save()
            
            messages.success(request, "Score created successfully!")

            return redirect("scoring_scores")

    context = {'form': form}

    return render(request, 'scoring/django/score/create.html', context=context)

@login_required(login_url='scoring/my-login')
def update_score(request, pk):
    score = Score.objects.get(id=pk)
    form = UpdateScoreForm(instance=score)

    if request.method == "POST":
        form = UpdateScoreForm(request.POST, instance=score)

        if form.is_valid():
            form.save()
            
            messages.success(request, "Score updated successfully!")

            return redirect("scoring_scores")

    context = {'form': form}

    return render(request, 'scoring/django/score/update.html', context=context)

@login_required(login_url='scoring/my-login')
def singular_score(request, pk):
    score = Score.objects.get(id=pk)
    context = {'score': score}

    return render(request, 'scoring/django/score/view.html', context)

@login_required(login_url='scoring/my-login')
def delete_score(request, pk):
    score = Score.objects.get(id=pk)
    score.delete()

    messages.success(request, "Score deleted successfully!")

    return redirect("scoring_scores")

# ScoringSheet

def scoringsheets(request):
    scoringsheets = ScoringSheet.objects.all()
    template = 'scoring/django/scoringsheet/index.html'
    context = {'scoringsheets': scoringsheets}

    return render(request, template, context)

@login_required(login_url='scoring/my-login')
def create_scoringsheet(request):
    form = CreateScoringSheetForm()
    if request.method == "POST":
        form = CreateScoringSheetForm(request.POST)

        if form.is_valid():
            form.save()
            
            messages.success(request, "Scoring Sheet created successfully!")

            return redirect("scoring_scoringsheets")

    context = {'form': form}

    return render(request, 'scoring/django/scoringsheet/create.html', context=context)

@login_required(login_url='scoring/my-login')
def update_scoringsheet(request, pk):
    scoringsheet = ScoringSheet.objects.get(id=pk)
    form = UpdateScoringSheetForm(instance=scoringsheet)

    if request.method == "POST":
        form = UpdateScoringSheetForm(request.POST, instance=scoringsheet)

        if form.is_valid():
            form.save()
            
            messages.success(request, "Scoring Sheet updated successfully!")

            return redirect("scoring_scoringsheets")

    context = {'form': form}

    return render(request, 'scoring/django/scoringsheet/update.html', context=context)

@login_required(login_url='scoring/my-login')
def singular_scoringsheet(request, pk):
    scoringsheet = ScoringSheet.objects.get(id=pk)
    context = {'scoringsheet': scoringsheet}

    return render(request, 'scoring/django/scoringsheet/view.html', context)

@login_required(login_url='scoring/my-login')
def delete_scoringsheet(request, pk):
    scoringsheet = ScoringSheet.objects.get(id=pk)
    scoringsheet.delete()

    messages.success(request, "Scoring Sheet deleted successfully!")

    return redirect("scoring_scoringsheets")

# TargetFace

def targetfaces(request):
    targetfaces = TargetFace.objects.all()
    template = 'scoring/django/targetface/index.html'
    context = {'targetfaces': targetfaces}

    return render(request, template, context)

@login_required(login_url='scoring/my-login')
def create_targetface(request):
    form = CreateTargetFaceForm()
    if request.method == "POST":
        form = CreateTargetFaceForm(request.POST)

        if form.is_valid():
            form.save()
            
            messages.success(request, "Target Face created successfully!")

            return redirect("scoring_targetfaces")

    context = {'form': form}

    return render(request, 'scoring/django/targetface/create.html', context=context)

@login_required(login_url='scoring/my-login')
def update_targetface(request, pk):
    targetface = TargetFace.objects.get(id=pk)
    form = UpdateTargetFaceForm(instance=targetface)

    if request.method == "POST":
        form = UpdateTargetFaceForm(request.POST, instance=targetface)

        if form.is_valid():
            form.save()
            
            messages.success(request, "Target Face updated successfully!")

            return redirect("scoring_targetfaces")

    context = {'form': form}

    return render(request, 'scoring/django/targetface/update.html', context=context)

@login_required(login_url='scoring/my-login')
def singular_targetface(request, pk):
    targetface = TargetFace.objects.get(id=pk)
    context = {'targetface': targetface}

    return render(request, 'scoring/django/targetface/view.html', context)

@login_required(login_url='scoring/my-login')
def delete_targetface(request, pk):
    targetface = TargetFace.objects.get(id=pk)
    targetface.delete()

    messages.success(request, "Target Face deleted successfully!")

    return redirect("scoring_targetfaces")

# Team

def teams(request):
    teams = Team.objects.all()
    template = 'scoring/django/team/index.html'
    context = {'teams': teams}

    return render(request, template, context)

@login_required(login_url='scoring/my-login')
def create_team(request):
    form = CreateTeamForm()
    if request.method == "POST":
        form = CreateTeamForm(request.POST)

        if form.is_valid():
            form.save()
            
            messages.success(request, "Team created successfully!")

            return redirect("scoring_teams")

    context = {'form': form}

    return render(request, 'scoring/django/team/create.html', context=context)

@login_required(login_url='scoring/my-login')
def update_team(request, pk):
    team = Team.objects.get(id=pk)
    form = UpdateTeamForm(instance=team)

    if request.method == "POST":
        form = UpdateTeamForm(request.POST, instance=team)

        if form.is_valid():
            form.save()
            
            messages.success(request, "Team updated successfully!")

            return redirect("scoring_teams")

    context = {'form': form}

    return render(request, 'scoring/django/team/update.html', context=context)

@login_required(login_url='scoring/my-login')
def singular_team(request, pk):
    team = Team.objects.get(id=pk)
    context = {'team': team}

    return render(request, 'scoring/django/team/view.html', context)

@login_required(login_url='scoring/my-login')
def delete_team(request, pk):
    team = Team.objects.get(id=pk)
    team.delete()

    messages.success(request, "Team deleted successfully!")

    return redirect("scoring_teams")

# Register a user

def register(request):
    form = CreateUserForm()
    
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            
            messages.success(request, "Account created successfully for " + form.cleaned_data.get('email'))

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

# - User logout

def user_logout(request):
    auth.logout(request)

    messages.success(request, "You have been logged out!")

    return redirect("scoring_my-login")

# - Dashboard

@login_required(login_url='scoring/my-login')
def dashboard(request):
    return render(request, 'scoring/django/dashboard.html')

# ------------------
# TODO: Begin ScoringWizard
# ------------------

def scoringwizards(request):
    scoringwizards = ScoringWizard.objects.all()
    template = 'scoring/django/scoring_wizard/index.html'
    context = {'scoringwizards': scoringwizards}

    return render(request, template, context)

@login_required(login_url='scoring/my-login')
def create_scoringwizard(request):
    form = ScoringWizardForm()
    if request.method == "POST":
        form = ScoringWizardForm(request.POST)

        if form.is_valid():
            form.save()
            
            messages.success(request, "Scoring Wizard created successfully!")

            return redirect("scoring_scoringwizards")

    context = {'form': form}

    return render(request, 'scoring/django/scoring_wizard/create.html', context=context)

@login_required(login_url='scoring/my-login')
def update_scoringwizard(request):
    pass

@login_required(login_url='scoring/my-login')
def singular_scoringwizard(request):
    pass

@login_required(login_url='scoring/my-login')
def delete_scoringwizard(request):
    pass

# -----------------
# TODO: End ScoringWizard
# -----------------

# -----------------
# TODO: Begin Environment
# -----------------

@login_required(login_url='scoring/my-login')
def environment(request):
    pass

@login_required(login_url='scoring/my-login')
def collection(request):
    pass

@login_required(login_url='scoring/my-login')
def solution(request):
    pass

# -----------------
# TODO: End Environment
# -----------------
