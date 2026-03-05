from django.contrib.auth.forms import UserCreationForm
from custom_user.models import User

from django import forms

from django.contrib.auth.forms import AuthenticationForm
from django.forms.widgets import PasswordInput, TextInput

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
    Team,
)

# Register/Create a user

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['email', 'password1', 'password2']

class LoginForm(AuthenticationForm):
    username = forms.EmailField(label="E-mail", widget=forms.EmailInput(attrs={'autofocus': True}))
    password = forms.CharField(widget=PasswordInput())

# AgeGroup

# - Create a agegroup
class CreateAgeGroupForm(forms.ModelForm):
    class Meta:
        model = AgeGroup
        fields = [
            'name', 'from_year', 'until_year', 'agegroups', 'info',
            'slug', 'author',
            'is_active',
        ]

# - Update a agegroup
class UpdateAgeGroupForm(forms.ModelForm):
    class Meta:
        model = AgeGroup
        fields = [
            'name', 'from_year', 'until_year', 'agegroups', 'info',
            'slug', 'author',
            'is_active',
        ]

# Archer

# - Create an archer
class CreateArcherForm(forms.ModelForm):
    class Meta:
        model = Archer
        fields = [
            'union_number', 'last_name', 'first_name', 'middle_name', 'info',
            'email', 'phone', 'address', 'city', 'zip_code', 'province',
            'birth_date', 'slug', 'author',
            'is_active',
        ]

class UpdateArcherForm(forms.ModelForm):
    class Meta:
        model = Archer
        fields = [
            'union_number', 'last_name', 'first_name', 'middle_name', 'info',
            'email', 'phone', 'address', 'city', 'zip_code', 'province',
            'birth_date', 'slug', 'author',
            'is_active',
        ]

# Category

class CreateCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = [
            'name', 'info',
            'slug', 'author',
            'is_active',
        ]

class UpdateCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = [
            'name', 'info',
            'slug', 'author',
            'is_active',
        ]

# Club

class CreateClubForm(forms.ModelForm):
    class Meta:
        model = Club
        fields = [
            'name', 'info',
            'address', 'zip_code', 'town', 'phone', 'email', 'website', 'social_media',
            'slug', 'author',
            'is_active',
        ]

class UpdateClubForm(forms.ModelForm):
    class Meta:
        model = Club
        fields = [
            'name', 'info',
            'address', 'zip_code', 'town', 'phone', 'email', 'website', 'social_media',
            'slug', 'author',
            'is_active',
        ]

# Competition

class CreateCompetitionForm(forms.ModelForm):
    class Meta:
        model = Competition
        fields = [
            'name', 'start_date', 'end_date', 'info',
            'slug', 'author',
            'is_active',
        ]

class UpdateCompetitionForm(forms.ModelForm):
    class Meta:
        model = Competition
        fields = [
            'name', 'start_date', 'end_date', 'info',
            'slug', 'author',
            'is_active',
        ]

# Discipline

class CreateDisciplineForm(forms.ModelForm):
    class Meta:
        model = Discipline
        fields = [
            'name', 'info',
            'slug', 'author',
            'is_active',
        ]

class UpdateDisciplineForm(forms.ModelForm):
    class Meta:
        model = Discipline
        fields = [
            'name', 'info',
            'slug', 'author',
            'is_active',
        ]

# Round

class CreateRoundForm(forms.ModelForm):
    class Meta:
        model = Round
        fields = [
            'name', 'start_date', 'start_time', 'end_date', 'end_time', 'info',
            'slug', 'author',
            'is_active',
        ]

class UpdateRoundForm(forms.ModelForm):
    class Meta:
        model = Round
        fields = [
            'name', 'start_date', 'start_time', 'end_date', 'end_time', 'info',
            'slug', 'author',
            'is_active',
        ]

# Score

class CreateScoreForm(forms.ModelForm):
    class Meta:
        model = Score
        fields = [
            'round_archer', 'score', 'number_of_arrows',
            'author', 'info',
        ]

class UpdateScoreForm(forms.ModelForm):
    class Meta:
        model = Score
        fields = [
            'round_archer', 'score', 'number_of_arrows',
            'author', 'info',
        ]

# ScoringSheet

class CreateScoringSheetForm(forms.ModelForm):
    class Meta:
        model = ScoringSheet
        fields = [
            'name', 'columns', 'rows', 'info',
            'slug', 'author',
            'is_active',
        ]

class UpdateScoringSheetForm(forms.ModelForm):
    class Meta:
        model = ScoringSheet
        fields = [
            'name', 'columns', 'rows', 'info',
            'slug', 'author',
            'is_active',
        ]

# TargetFace

class CreateTargetFaceForm(forms.ModelForm):
    class Meta:
        model = TargetFace
        fields = [
            'name', 'info',
            'slug', 'author',
            'is_active',
        ]
class UpdateTargetFaceForm(forms.ModelForm):
    class Meta:
        model = TargetFace
        fields = [
            'name', 'info',
            'slug', 'author',
            'is_active',
        ]

# Team

class CreateTeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = [
            'name', 'info',
            'slug', 'author',
            'is_active',
        ]

class UpdateTeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = [
            'name', 'info',
            'slug', 'author',
            'is_active',
        ]
