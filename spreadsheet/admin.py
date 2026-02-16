from django.contrib import admin

from .models import Workbook, Worksheet

@admin.action(description="Activate selected Workbooks")
def activate_workbooks(modeladmin, request, queryset):
    queryset.update(is_active=True)

@admin.action(description="Deactivate selected Workbooks")
def deactivate_workbooks(modeladmin, request, queryset):
    queryset.update(is_active=False)

@admin.register(Workbook)
class WorkbookAdmin(admin.ModelAdmin):
    actions = [activate_workbooks, deactivate_workbooks]
    list_display = ('name',)
    filter_horizontal = ('worksheets',)

@admin.action(description="Activate selected Worksheets")
def activate_worksheets(modeladmin, request, queryset):
    queryset.update(is_active=True)

@admin.action(description="Deactivate selected Worksheets")
def deactivate_worksheets(modeladmin, request, queryset):
    queryset.update(is_active=False)

@admin.register(Worksheet)
class WorksheetAdmin(admin.ModelAdmin):
    actions = [activate_worksheets, deactivate_worksheets]
    list_display = ('name',)

