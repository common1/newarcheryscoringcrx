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
