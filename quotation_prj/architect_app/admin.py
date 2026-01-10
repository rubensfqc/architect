from django.contrib import admin
from .models import Architect, Contract, Project
# Register your models here.

class ProjectInline(admin.TabularInline):
    model = Project
    extra = 1
    fields = ('name', 'location', 'expected_completion_date', 'completion_date')


@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display = ('title', 'architect', 'client', 'start_date', 'end_date')
    list_filter = ('architect', 'start_date')
    search_fields = ('title', 'client__user__email')
    inlines = [ProjectInline]


class ContractInline(admin.TabularInline):
    model = Contract
    extra = 0
    fields = ('title', 'client', 'start_date', 'end_date')

@admin.register(Architect)
class ArchitectAdmin(admin.ModelAdmin):
    list_display = ('user', 'firm_name', 'license_number')
    search_fields = ('user__email', 'firm_name', 'license_number')
    inlines = [ContractInline]
