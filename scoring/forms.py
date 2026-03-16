from django.contrib.auth.forms import UserCreationForm
from custom_user.models import User

from django import forms

from django.contrib.auth.forms import AuthenticationForm
from django.forms.widgets import PasswordInput, TextInput
from django.utils.translation import gettext_lazy as _

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

from .widgets import (
    DatePickerInput,
    TimePickerInput,
    DateTimePickerInput,
    YEAR_CHOICES,
)

from calendar import Calendar

from datetime import datetime

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
    info = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'rows': 4}),
    )
    agegroups = forms.ModelMultipleChoiceField(
        queryset = AgeGroup.objects.all(),
        required=False,
        label="Agegroups",
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = AgeGroup
        fields = [
            'name', 'from_year', 'until_year', 'info',
            'slug', 'author',
            'agegroups', 
        ]

# - Update a agegroup
class UpdateAgeGroupForm(forms.ModelForm):
    info = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'rows': 4}),
    )
    agegroups = forms.ModelMultipleChoiceField(
        queryset = AgeGroup.objects.all(),
        required=False,
        label="Agegroups",
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = AgeGroup
        fields = [
            'name', 'from_year', 'until_year','info',
            'slug', 'author',
            'agegroups', 
        ]

# Archer

# - Create an archer
class CreateArcherForm(forms.ModelForm):
    info = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'rows': 4}),
    )
    birth_date = forms.DateField(
        widget=forms.SelectDateWidget(
            empty_label=("Year", "Month", "Day"),
            years=range(1940, datetime.now().year + 10),
            attrs=({'style': 'width: 33%; display: inline-block;'}),
        ),
        help_text=_("format: not required"),
        required=False,
    )

    class Meta:
        model = Archer
        fields = [
            'union_number', 'last_name', 'first_name', 'middle_name', 'info',
            'email', 'phone', 'address', 'city', 'zip_code', 'province',
            'birth_date', 'slug', 'author',
        ]

class UpdateArcherForm(forms.ModelForm):
    info = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'rows': 4}),
    )
    birth_date = forms.DateField(
        widget=forms.SelectDateWidget(
            empty_label=("Year", "Month", "Day"),
            years=range(1940, datetime.now().year + 10),
            attrs=({'style': 'width: 33%; display: inline-block;'}),
        ),
        help_text=_("format: not required"),
        required=False,
    )

    class Meta:
        model = Archer
        fields = [
            'union_number', 'last_name', 'first_name', 'middle_name', 'info',
            'email', 'phone', 'address', 'city', 'zip_code', 'province',
            'birth_date', 'slug', 'author',
        ]

# Category

class CreateCategoryForm(forms.ModelForm):
    info = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'rows': 4}),
    )
    archers = forms.ModelMultipleChoiceField(
        queryset = Archer.objects.all(),
        label="Archers",
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Category
        fields = [
            'name', 'info',
            'slug', 'author',
            'archers',
        ]

class UpdateCategoryForm(forms.ModelForm):
    info = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'rows': 4}),
    )
    archers = forms.ModelMultipleChoiceField(
        queryset = Archer.objects.all(),
        label="Archers",
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Category
        fields = [
            'name', 'info',
            'slug', 'author',
            'archers',
        ]

# Club

class CreateClubForm(forms.ModelForm):
    info = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'rows': 4}),
    )
    archers = forms.ModelMultipleChoiceField(
        queryset = Archer.objects.all(),
        label="Archers",
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Club
        fields = [
            'name', 'info',
            'address', 'zip_code', 'town', 'phone', 'email', 'website', 'social_media',
            'slug', 'author',
            'archers',
        ]

class UpdateClubForm(forms.ModelForm):
    info = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'rows': 4}),
    )
    archers = forms.ModelMultipleChoiceField(
        queryset = Archer.objects.all(),
        label="Archers",
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Club
        fields = [
            'name', 'info',
            'address', 'zip_code', 'town', 'phone', 'email', 'website', 'social_media',
            'slug', 'author',
            'archers',
        ]

# Competition

class CreateCompetitionForm(forms.ModelForm):
    info = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'rows': 4}),
    )
    rounds = forms.ModelMultipleChoiceField(
        queryset = Round.objects.all(),
        label="Rounds",
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Competition
        fields = [
            'name', 'start_date', 'end_date', 'info',
            'slug', 'author',
            'rounds',
        ]

class UpdateCompetitionForm(forms.ModelForm):
    info = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'rows': 4}),
    )
    rounds = forms.ModelMultipleChoiceField(
        queryset = Round.objects.all(),
        label="Rounds",
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Competition
        fields = [
            'name', 'start_date', 'end_date', 'info',
            'slug', 'author',
            'rounds',
        ]

# Discipline

class CreateDisciplineForm(forms.ModelForm):
    info = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'rows': 4}),
    )
    archers = forms.ModelMultipleChoiceField(
        queryset = Archer.objects.all(),
        label="Archers",
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Discipline
        fields = [
            'name', 'info',
            'slug', 'author',
            'archers',
        ]

class UpdateDisciplineForm(forms.ModelForm):
    info = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'rows': 4}),
    )
    archers = forms.ModelMultipleChoiceField(
        queryset = Archer.objects.all(),
        label="Archers",
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Discipline
        fields = [
            'name', 'info',
            'slug', 'author',
            'archers',
        ]

# Round

class CreateRoundForm(forms.ModelForm):
    info = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'rows': 4}),
    )
    archers = forms.ModelMultipleChoiceField(
        queryset = Archer.objects.all(),
        label="Archers",
        widget=forms.CheckboxSelectMultiple
    )
    start_date = forms.DateField(
        widget=forms.SelectDateWidget(
            empty_label=("-Year-", "-Month-", "-Day-"),
            years=range(1940, datetime.now().year + 10),
            attrs=({'style': 'width: 33%; display: inline-block;'}),
        ),
        help_text=_("Not required"),
        required=False,
    )
    start_time = forms.TimeField(
        widget=forms.TimeInput(attrs={'type': 'time'}),
        help_text=_("Not required"),
        required=False,
    )
    end_date = forms.DateField(
        widget=forms.SelectDateWidget(
            empty_label=("-Year-", "-Month-", "-Day-"),
            years=range(1940, datetime.now().year + 10),
            attrs=({'style': 'width: 33%; display: inline-block;'}),
        ),
        help_text=_("Not required"),
        required=False,
    )
    end_time = forms.TimeField(
        widget=forms.TimeInput(attrs={'type': 'time'}),
        help_text=_("Not required"),
        required=False,
    )

    class Meta:
        model = Round
        fields = [
            'name', 'start_date', 'start_time', 'end_date', 'end_time', 'info',
            'slug', 'author',
            'archers',
        ]

class UpdateRoundForm(forms.ModelForm):
    info = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'rows': 4}),
    )
    archers = forms.ModelMultipleChoiceField(
        queryset = Archer.objects.all(),
        label="Archers",
        widget=forms.CheckboxSelectMultiple
    )
    start_date = forms.DateField(
        widget=forms.SelectDateWidget(
            empty_label=("-Year-", "-Month-", "-Day-"),
            years=range(1940, datetime.now().year + 10),
            attrs=({'style': 'width: 33%; display: inline-block;'}),
        ),
        help_text=_("Not required"),
        required=False,
    )
    start_time = forms.TimeField(
        widget=forms.TimeInput(attrs={'type': 'time'}),
        help_text=_("Not required"),
        required=False,
    )
    end_date = forms.DateField(
        widget=forms.SelectDateWidget(
            empty_label=("-Year-", "-Month-", "-Day-"),
            years=range(1940, datetime.now().year + 10),
            attrs=({'style': 'width: 33%; display: inline-block;'}),
        ),
        help_text=_("Not required"),
        required=False,
    )
    end_time = forms.TimeField(
        widget=forms.TimeInput(attrs={'type': 'time'}),
        help_text=_("Not required"),
        required=False,
    )

    class Meta:
        model = Round
        fields = [
            'name', 'start_date', 'start_time', 'end_date', 'end_time', 'info',
            'slug', 'author',
            'archers',
        ]

# Score

class CreateScoreForm(forms.ModelForm):
    info = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'rows': 4}),
    )

    class Meta:
        model = Score
        fields = [
            'round_archer', 'score', 'number_of_arrows',
            'author', 'info',
        ]

class UpdateScoreForm(forms.ModelForm):
    info = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'rows': 4}),
    )

    class Meta:
        model = Score
        fields = [
            'round_archer', 'score', 'number_of_arrows',
            'author', 'info',
        ]

# ScoringSheet

class CreateScoringSheetForm(forms.ModelForm):
    info = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'rows': 4}),
    )

    class Meta:
        model = ScoringSheet
        fields = [
            'name', 'columns', 'rows', 'info',
            'slug', 'author',
        ]

class UpdateScoringSheetForm(forms.ModelForm):
    info = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'rows': 4}),
    )

    class Meta:
        model = ScoringSheet
        fields = [
            'name', 'columns', 'rows', 'info',
            'slug', 'author',
        ]

# TargetFace

class CreateTargetFaceForm(forms.ModelForm):
    info = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'rows': 4}),
    )

    class Meta:
        model = TargetFace
        fields = [
            'name', 'info',
            'slug', 'author',
        ]
class UpdateTargetFaceForm(forms.ModelForm):
    info = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'rows': 4}),
    )

    class Meta:
        model = TargetFace
        fields = [
            'name', 'info',
            'slug', 'author',
        ]

# Team

class CreateTeamForm(forms.ModelForm):
    info = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'rows': 4}),
    )

    archers = forms.ModelMultipleChoiceField(
        queryset = Archer.objects.all(),
        label="Archers",
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Team
        fields = [
            'name', 'info',
            'slug', 'author',
            'archers', 
        ]

class UpdateTeamForm(forms.ModelForm):
    info = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'rows': 4}),
    )

    archers = forms.ModelMultipleChoiceField(
        queryset = Archer.objects.all(),
        label="Archers",
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Team
        fields = [
            'name', 'info',
            'slug', 'author',
            'archers', 
        ]
