from django.conf import settings
from django.contrib import admin
from django.db import models
from django import forms
from .models import (
    Archer,
    AgeGroup,
    Category,
    CategoryMembership,
    Club,
    ClubMembership,
    Competition,
    CompetitionMembership,
    Discipline,
    DisciplineMembership,
    Round,
    RoundMembership,
    TargetFaceNameChoice,
    TargetFace,
    Team,
    TeamMembership,
    Score,
    ScoringSheet,
    
    ScoringWizard,
    
    Environment,
    Collection,
    Solution,
)
from modelcluster.fields import ParentalKey

@admin.action(description="Activate selected Archers")
def activate_archers(modeladmin, request, queryset):
    queryset.update(is_active=True)

@admin.action(description="Deactivate selected Archers")
def deactivate_archers(modeladmin, request, queryset):
    queryset.update(is_active=False)

@admin.register(Archer)
class ArcherAdmin(admin.ModelAdmin):
    actions=[activate_archers, deactivate_archers]
    list_display = ('last_name', 'first_name', 'middle_name', 'union_number', 'is_active')
    list_editable = ('is_active',)
    list_filter = ('is_active',)
    list_display_links = ('last_name', 'first_name')
    list_per_page = 20
    ordering = ('last_name', 'first_name')
    fieldsets = (
        (None, {
            'fields': ( 'union_number', 'last_name', 'first_name', 'middle_name', 'info',)
        }),
        ('Contact Information', {
            'classes': ['collapse'],
            'fields': ('email', 'phone', 'address', 'city', 'zip_code', 'province',),
        }),
        ('Extra Information', {
            'classes': ['collapse'],
            'fields': ('birth_date', 'slug', 'author'),
        }),
        ('Special', {
            'classes': ['collapse'],
            'fields': ('is_active',),
        }),
    )
    search_fields = ('last_name', 'first_name', 'info')

@admin.action(description="Activate selected Age Groups")
def activate_agegroups(modeladmin, request, queryset):
    queryset.update(is_active=True)

@admin.action(description="Deactivate selected Age Groups")
def deactivate_agegroups(modeladmin, request, queryset):
    queryset.update(is_active=False)

@admin.register(AgeGroup)
class AgeGroupAdmin(admin.ModelAdmin):
    actions=[activate_agegroups, deactivate_agegroups]
    list_display = ('name', 'is_active',)
    list_editable = ('is_active',)
    list_filter = ('is_active',)
    list_display_links = ('name',)
    list_per_page = 20
    # ordering = ('-id',)
    # list_editable = ('is_active',)
    filter_horizontal = ('agegroups',)
    fieldsets = (
        (None, {
            'fields': ('name', 'from_year', 'until_year', 'agegroups', 'info',)
        }),
        ('Extra Information', {
            'classes': ['collapse'],
            'fields': (
                'slug', 
                'author', 
            ),
        }),
        ('Special', {
            'classes': ['collapse'],
            'fields': ('is_active',),
        }),
    )
    search_fields = ('name', 'info')

@admin.action(description="Activate selected Clubs")
def activate_clubs(modeladmin, request, queryset):
    queryset.update(is_active=True)

@admin.action(description="Deactivate selected Clubs")
def deactivate_clubs(modeladmin, request, queryset):
    queryset.update(is_active=False)

class ClubMembershipInline(admin.TabularInline):
    model = ClubMembership
    extra = 1
    fields = ('archer', 'start_date', 'end_date')
    can_delete = True
    show_change_link = True
    
@admin.register(Club)
class ClubAdmin(admin.ModelAdmin):
    actions=[activate_clubs, deactivate_clubs]
    inlines = [
        ClubMembershipInline
    ]
    list_display = ('name', 'town', 'is_active',)
    list_editable = ('is_active',)
    list_filter = ('is_active',)
    list_display_links = ('name', 'town')
    list_per_page = 20
    ordering = ('name',)
    # list_editable = ('is_active',)
    fieldsets = (
        (None, {
            'fields': ('name', 'info')
        }),
        ('Contact Information', {
            'classes': ['collapse'],
            'fields': (
                'address', 
                'zip_code', 
                'town',
                'phone',
                'email',
                'website',
                'social_media',
            ),
        }),
        ('Extra Information', {
            'classes': ['collapse'],
            'fields': ('slug', 'author'),
        }),
        ('Special', {
            'classes': ['collapse'],
            'fields': ('is_active',),
        }),
    )
    search_fields = ('name', 'town')

@admin.action(description="Activate selected Club Memberships")
def activate_clubmemberships(modeladmin, request, queryset):
    queryset.update(is_active=True)

@admin.action(description="Deactivate selected Club Memberships")
def deactivate_clubmemberships(modeladmin, request, queryset):
    queryset.update(is_active=False)

@admin.register(ClubMembership)
class ClubMembershipAdmin(admin.ModelAdmin):
    actions=[activate_clubmemberships, deactivate_clubmemberships]
    list_display = ('archer', 'club', 'start_date', 'end_date', 'is_active')
    list_editable = ('is_active',)
    list_filter = ('is_active', 'archer',)
    list_display_links = ('archer',)
    list_per_page = 20
    ordering = ('club', 'archer',)
    fieldsets = (
        (None, {
            'fields': ('club','archer', 'info')
        }),
        ('Extra Information', {
            'classes': ['collapse'],
            'fields': (
                'slug', 
                'author',
                'start_date', 
                'end_date',
            ),
        }),
        ('Special', {
            'classes': ['collapse'],
            'fields': ('is_active',),
        }),
    )
    search_fields = ('archer__last_name', 'club__name')

@admin.action(description="Activate selected Categories")
def activate_categories(modeladmin, request, queryset):
    queryset.update(is_active=True)

@admin.action(description="Deactivate selected Categories")
def deactivate_categories(modeladmin, request, queryset):
    queryset.update(is_active=False)

class CategoryMembershipInline(admin.TabularInline):
    model = CategoryMembership
    extra = 1
    fields = ('category', 'archer', 'agegroup')
    can_delete = True
    show_change_link = True

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    actions=[activate_categories, deactivate_categories]
    inlines = [
        CategoryMembershipInline
    ]
    list_display = ('name', 'is_active',)
    list_editable = ('is_active',)
    list_filter = ('is_active',)
    list_display_links = ('name',)
    list_per_page = 20
    ordering = ('name',)
    fieldsets = (
        (None, {
            'fields': ('name', 'info',)
        }),
        ('Extra Information', {
            'classes': ['collapse'],
            'fields': (
                'slug', 
                'author', 
            ),
        }),
        ('Special', {
            'classes': ['collapse'],
            'fields': ('is_active',),
        }),
    )
    search_fields = ('name', 'info')

@admin.action(description="Activate selected Category Memberships")
def activate_category_memberships(modeladmin, request, queryset):
    queryset.update(is_active=True)

@admin.action(description="Deactivate selected Category Memberships")
def deactivate_category_memberships(modeladmin, request, queryset):
    queryset.update(is_active=False)

@admin.register(CategoryMembership)
class CategoryMembershipAdmin(admin.ModelAdmin):
    actions=[activate_category_memberships, deactivate_category_memberships]
    list_display = ('category', 'archer', 'agegroup', 'is_active',)
    list_editable = ('is_active',)
    list_filter = ('is_active', 'archer',)
    list_display_links = ('category', 'archer',)
    list_per_page = 20
    ordering = ('category', 'archer')
    fieldsets = (
        (None, {
            'fields': (
                'category', 
                'archer', 
                'agegroup', 
                'info', 
            )
        }),
        ('Extra Information', {
            'classes': ['collapse'],
            'fields': ('slug', 'author'),
        }),
        ('Special', {
            'classes': ['collapse'],
            'fields': ('is_active',),
        }),
    )
    search_fields = ('category__name', 'archer__name')

@admin.action(description="Activate selected Disciplines")
def activate_disciplines(modeladmin, request, queryset):
    queryset.update(is_active=True)

@admin.action(description="Deactivate selected Disciplines")
def deactivate_disciplines(modeladmin, request, queryset):
    queryset.update(is_active=False)

class DisciplineMembershipInline(admin.TabularInline):
    model = DisciplineMembership
    extra = 1
    fields = ('discipline', 'archer',)
    can_delete = True
    show_change_link = True
    
@admin.register(Discipline)
class DisciplineAdmin(admin.ModelAdmin):
    actions=[activate_disciplines, deactivate_disciplines]
    inlines = [
        DisciplineMembershipInline
    ]
    list_display = ('name', 'is_active',)
    list_editable = ('is_active',)
    list_filter = ('is_active',)
    list_display_links = ('name',)
    list_per_page = 20
    ordering = ('name',)
    fieldsets = (
        (None, {
            'fields': ('name', 'info',)
        }),
        ('Extra Information', {
            'classes': ['collapse'],
            'fields': (
                'slug', 
                'author', 
            ),
        }),
        ('Special', {
            'classes': ['collapse'],
            'fields': ('is_active',),
        }),
    )
    search_fields = ('name', 'info')

@admin.action(description="Activate selected Discipline Memberships")
def activate_discipline_memberships(modeladmin, request, queryset):
    queryset.update(is_active=True)

@admin.action(description="Deactivate selected Discipline Memberships")
def deactivate_discipline_memberships(modeladmin, request, queryset):
    queryset.update(is_active=False)

@admin.register(DisciplineMembership)
class DisciplineMembershipAdmin(admin.ModelAdmin):
    actions=[activate_discipline_memberships, deactivate_discipline_memberships]
    list_display = ('discipline', 'archer', 'is_active',)
    list_editable = ('is_active',)
    list_filter = ('discipline', 'archer', 'is_active',)
    list_display_links = ('discipline', 'archer',)
    list_per_page = 20
    ordering = ('discipline', 'archer',)
    fieldsets = (
        (None, {
            'fields': (
                'discipline', 
                'archer', 
                'info', 
            )
        }),
        ('Extra Information', {
            'classes': ['collapse'],
            'fields': ('slug', 'author'),
        }),
        ('Special', {
            'classes': ['collapse'],
            'fields': ('is_active',),
        }),
    )
    search_fields = ('discipline__name', 'archer__last_name',)

@admin.action(description="Activate selected Teams")
def activate_teams(modeladmin, request, queryset):
    queryset.update(is_active=True)

@admin.action(description="Deactivate selected Teams")
def deactivate_teams(modeladmin, request, queryset):
    queryset.update(is_active=False)

class TeamMembershipInline(admin.TabularInline):
    model = TeamMembership
    extra = 1
    fields = ('team', 'archer',)
    can_delete = True
    show_change_link = True

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    actions=[activate_teams, deactivate_teams]
    inlines = [
        TeamMembershipInline
    ]
    list_display = ('name', 'is_active',)
    list_editable = ('is_active',)
    list_filter = ('is_active',)
    list_display_links = ('name',)
    list_per_page = 20
    ordering = ('name',)
    fieldsets = (
        (None, {
            'fields': ('name', 'info',)
        }),
        ('Extra Information', {
            'classes': ['collapse'],
            'fields': ('slug', 'author',),
        }),
        ('Special', {
            'classes': ['collapse'],
            'fields': ('is_active',),
        }),
    )
    search_fields = ('name',)

admin.action(description="Activate selected Team Memberships")
def activate_team_memberships(modeladmin, request, queryset):
    queryset.update(is_active=True)

@admin.action(description="Deactivate selected Team Memberships")
def deactivate_team_memberships(modeladmin, request, queryset):
    queryset.update(is_active=False)

@admin.register(TeamMembership)
class TeamMembershipAdmin(admin.ModelAdmin):
    actions=[activate_team_memberships, deactivate_team_memberships]
    list_display = ('team', 'archer', 'is_active',)
    list_editable = ('is_active',)
    list_filter = ('is_active',)
    list_display_links = ('team', 'archer',)
    list_per_page = 20
    ordering = ('team', 'archer',)
    fieldsets = (
        (None, {
            'fields': ('team', 'archer', 'info',)
        }),
        ('Extra Information', {
            'classes': ['collapse'],
            'fields': ('slug', 'author',),
        }),
        ('Special', {
            'classes': ['collapse'],
            'fields': ('is_active',),
        }),
    )
    search_fields = ('team__name', 'archer__name')

@admin.action(description="Activate selected Scoring Sheets")
def activate_scoring_sheets(modeladmin, request, queryset):
    queryset.update(is_active=True)

@admin.action(description="Deactivate selected Scoring Sheets")
def deactivate_scoring_sheets(modeladmin, request, queryset):
    queryset.update(is_active=False)
 
@admin.register(ScoringSheet)
class ScoringSheetAdmin(admin.ModelAdmin):
    actions=[activate_scoring_sheets, deactivate_scoring_sheets]
    list_display = ('name', 'columns', 'rows', 'is_active',)
    list_editable = ('is_active',)
    list_filter = ('is_active',)
    list_display_links = ('name',)
    list_per_page = 20
    ordering = ('name',)
    fieldsets = (
        (None, {
            'fields': ('name', 'columns', 'rows', 'info',)
        }),
        ('Extra Information', {
            'classes': ['collapse'],
            'fields': ('slug', 'author',),
        }),
        ('Special', {
            'classes': ['collapse'],
            'fields': ('is_active',),
        }),
    )
    search_fields = ('name', 'info')

class TargetFaceNameChoiceAdminForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):        
        super().__init__(*args, **kwargs)
        
    class Meta:
        model = TargetFaceNameChoice
        exclude = ('id',)

    def clean(self):
        data = self.cleaned_data
        
        # if not ('environment' in data.keys() or 'discipline' in data.keys() or 'targetsize' in data.keys() or 'keyfeature' in data.keys()):
        #     raise forms.ValidationError("Please fill out missing fields.")

        if ('environment' in data.keys() and 'discipline' in data.keys() and 'targetsize' in data.keys() and 'keyfeature' in data.keys()): 
            environment = data['environment']
            discipline = data['discipline']
            targetsize = data['targetsize']
            keyfeature = data['keyfeature']
            new_name = f"{environment} {discipline} {targetsize} {keyfeature}"
            if TargetFaceNameChoice.objects.filter(name=new_name):
                raise forms.ValidationError(f"Name '{new_name}' already exists.")
            else:
                self.cleaned_data['name'] = new_name
                self.instance.name = new_name
    
        return data
    
@admin.register(TargetFaceNameChoice)
class TargetFaceNameChoiceAdmin(admin.ModelAdmin):
    form = TargetFaceNameChoiceAdminForm
    list_display=('name', 'is_active',)
    list_editable = ('is_active',)
    list_filter=('is_active',)
    list_display_links=('name',)
    list_per_page=20
    ordering=('name',)
    readonly_fields=('name',)
    fieldsets = (
        (None, {
            'fields': (
                'name',
                'environment',
                'discipline',
                'targetsize',
                'keyfeature',
                'info',
            )
        }),
        ('Extra Information', {
            'classes': ['collapse'],
            'fields': ('slug', 'author',),
        }),
        ('Special', {
            'classes': ['collapse'],
            'fields': ('is_active',),
        }),
    )
    search_fields = ('name', 'info')

class TargetFaceAdminForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):        
        super().__init__(*args, **kwargs)

    class Meta:
        model = TargetFace
        exclude = ('id',)

    def set_choices():
        CHOICES = []
        CHOICES.append((None, None),)
        
        objs = TargetFaceNameChoice.objects.all()
        if objs:
            for obj in objs:
                CHOICES.append((obj.name, obj.name),)    
        return CHOICES

    name = forms.ChoiceField(choices=set_choices)
            
@admin.register(TargetFace)
class TargetFaceAdmin(admin.ModelAdmin):
    form=TargetFaceAdminForm
    list_display = ('name', 'is_active',)
    list_editable = ('is_active',)
    list_filter = ('is_active',)
    list_display_links = ('name',)
    list_per_page = 20
    ordering = ('name',)
    fieldsets = (
        (None, {
            'fields': ('name', 'info',)
        }),
        ('Extra Information', {
            'classes': ['collapse'],
            'fields': (
                'slug', 
                'author', 
            ),
        }),
        ('Special', {
            'classes': ['collapse'],
            'fields': ('is_active',),
        }),
    )
    search_fields = ('name', 'info')

@admin.action(description="Activate selected Rounds")
def activate_selected_rounds(modeladmin, request, queryset):
    queryset.update(is_active=True)

@admin.action(description="Deactivate selected Rounds")
def deactivate_selected_rounds(modeladmin, request, queryset):
    queryset.update(is_active=False)

# TODO: Scores_for_selected_rounds
@admin.action(description="Scores for selected Rounds")
def scores_for_selected_rounds(modeladmin, request, queryset):
    # for obj in queryset:
    #     print(obj.id)
    round_memberships = RoundMembership.objects.all()
    print(round_memberships)

class RoundMembershipInline(admin.TabularInline):
    model = RoundMembership
    extra=1
    fields = ('archer',)
    can_delete = True
    show_change_link = False

@admin.register(Round)
class RoundAdmin(admin.ModelAdmin):
    actions = [
        activate_selected_rounds, 
        deactivate_selected_rounds,
        scores_for_selected_rounds,
    ]
    inlines = [
        RoundMembershipInline,
    ]
    list_display = (
        'name', 'start_date', 'start_time', 'end_date', 'end_time', 'is_active',
    )
    list_editable = ('is_active',)
    list_filter = ('is_active',)
    list_display_links = ('name',)
    list_per_page = 20
    ordering = ('name',)
    search_fields = ('name', 'info',)
    fieldsets = (
        (None, {
            'fields': ('name', 'start_date', 'start_time', 'end_date', 'end_time', 'info',)
        }),
        ('Extra Information', {
            'classes': ['collapse'],
            'fields': ('slug', 'author',),
        }),
        ('Special', {
            'classes': ['collapse'],
            'fields': ('is_active',),
        }),
    )

@admin.action(description="Activate selected Round Memberships")
def activate_round_memberships(modeladmin, request, queryset):
    queryset.update(is_active=True)

@admin.action(description="Deactivate selected Round Memberships")
def deactivate_round_memberships(modeladmin, request, queryset):
    queryset.update(is_active=False)

@admin.register(RoundMembership)
class RoundMembershipAdmin(admin.ModelAdmin):
    actions=[activate_round_memberships, deactivate_round_memberships]
    list_display = ('round', 'archer', 'is_active',)
    list_editable = ('is_active',)
    list_filter = ('is_active',)
    list_display_links = ('round', 'archer',)
    list_per_page = 20
    ordering = ('round', 'archer',)
    fieldsets = (
        (None, {
            'fields': ('round', 'archer', 'info',)
        }),
        ('Extra Information', {
            'classes': ['collapse'],
            'fields': ('slug', 'author',),
        }),
        ('Special', {
            'classes': ['collapse'],
            'fields': ('is_active',),
        }),
    )
    search_fields = ('round__name', 'archer__name')

@admin.register(Score)
class ScoreAdmin(admin.ModelAdmin):
    def round_name(self, obj):
        if obj.round_archer:
            return obj.round_archer.round.name
        else:
            return "No Round"
    
    def archer_name(self, obj):
        if obj.round_archer:
            return obj.round_archer.archer
        else:
            return "No Archer"
    
    list_display = (
        'archer_name',
        'score', 
        'round_name',
        'is_active',
    )
    # list_display_links = ('score',)
    list_editable = ('score',)
    list_per_page = 20
    list_filter = ('is_active', 'round_archer__round',)
    fieldsets = (
        (None, {
            'fields': (
                'round_archer',
                'score',
                'number_of_arrows',
            )
        }),
        ('Extra Information', {
            'classes': ['collapse'],
            'fields': (
                'author',
                'info', 
            ),
        }),
    )

@admin.action(description="Activate selected Competitions")
def activate_competitions(modeladmin, request, queryset):
    queryset.update(is_active=True)

@admin.action(description="Deactivate selected Competitions")
def deactivate_competitions(modeladmin, request, queryset):
    queryset.update(is_active=False)

class CompetitionMembershipInline(admin.TabularInline):
    model = CompetitionMembership
    extra = 1
    fields = ('competition', 'round',)
    can_delete = True
    show_change_link = True

@admin.register(Competition)
class CompetitionAdmin(admin.ModelAdmin):
    actions=[
        activate_competitions, 
        deactivate_competitions
    ]
    inlines = [
        CompetitionMembershipInline
    ]
    list_display = (
        'name', 'start_date', 'end_date', 'is_active',
    )
    list_editable = ('is_active',)
    list_filter = ('is_active',)
    list_display_links = ('name',)
    list_per_page = 20
    ordering = ('name',)
    search_fields = ('name', 'info',)
    fieldsets = (
        (None, {
            'fields': ('name', 'start_date', 'end_date', 'info',)
        }),
        ('Extra Information', {
            'classes': ['collapse'],
            'fields': ('slug', 'author',),
        }),
        ('Special', {
            'classes': ['collapse'],
            'fields': ('is_active',),
        }),
    )

@admin.action(description="Activate selected Competition Memberships")
def activate_competition_memberships(modeladmin, request, queryset):
    queryset.update(is_active=True)

@admin.action(description="Deactivate selected Competition Memberships")
def deactivate_competition_memberships(modeladmin, request, queryset):
    queryset.update(is_active=False)

@admin.register(CompetitionMembership)
class CompetitionMembershipAdmin(admin.ModelAdmin):
    actions=[activate_competition_memberships, deactivate_competition_memberships]
    list_display = ('competition', 'round', 'is_active',)
    list_editable = ('is_active',)
    list_filter = ('is_active',)
    list_display_links = ('competition', 'round',)
    list_per_page = 20
    ordering = ('competition', 'round',)
    fieldsets = (
        (None, {
            'fields': ('competition', 'round', 'info',)
        }),
        ('Extra Information', {
            'classes': ['collapse'],
            'fields': ('slug', 'author',),
        }),
        ('Special', {
            'classes': ['collapse'],
            'fields': ('is_active',),
        }),
    )
    search_fields = ('round__name', 'round__name')

# ------------------------------
# TODO: Begin ScoringWizard Admin
# ------------------------------

@admin.action(description="Activate selected Scoring Wizards")
def activate_scoring_wizards(modeladmin, request, queryset):
    queryset.update(is_active=True)

@admin.action(description="Deactivate selected Scoring Wizards")
def deactivate_scoring_wizards(modeladmin, request, queryset):
    queryset.update(is_active=False)

@admin.register(ScoringWizard)
class ScoringWizardAdmin(admin.ModelAdmin):
    actions=[activate_scoring_wizards, deactivate_scoring_wizards]
    list_display = ('name', 'scoring_type', 'is_active',)
    list_editable = ('is_active',)
    list_filter = ('is_active',)
    list_display_links = ('name',)
    list_per_page = 20
    fieldsets = (
        (None, {
            'fields': ('name', 'info',)
        }),
        ('Scoring Wizard Specific', {
            'fields': (
                'title', 
                'sub_title', 
            ),
        }),
        ('Extra Information', {
            'classes': ['collapse'],
            'fields': (
                'slug', 
                'author', 
            ),
        }),
        ('Special', {
            'classes': ['collapse'],
            'fields': ('is_active',),
        }),
    )
    search_fields = ('name', 'info')

# ------------------------------
# TODO: End ScoringWizard Admin
# ------------------------------

# -----------------------------
# TODO: Begin Environment Admin
# -----------------------------

@admin.register(Environment)
class EnvironmentAdmin(admin.ModelAdmin):
    pass

@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    pass

@admin.register(Solution)
class SolutionAdmin(admin.ModelAdmin):
    pass

# ---------------------------
# TODO: End Environment Admin
# ---------------------------
