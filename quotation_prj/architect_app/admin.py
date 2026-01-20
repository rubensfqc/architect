from django.contrib import admin
from .models import Architect, Contract, Project, ClientProfile, Operator
# Register your models here.

class ProjectInline(admin.TabularInline):
    model = Project
    extra = 1
    fields = ('name', 'location', 'expected_completion_date', 'completion_date')


@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display = ('title', 'architect', 'client', 'phase', 'progress_percentage', 'is_active')
    list_filter = ('phase', 'is_active', 'architect')
    search_fields = ('title', 'client__user__email')
    # Organiza campos em seções no formulário de edição
    fieldsets = (
        (None, {'fields': ('title', 'architect', 'client')}),
        ('Status', {'fields': ('phase', 'progress_percentage', 'is_active')}),
        ('Valores e Datas', {'fields': ('budget', 'start_date', 'end_date')}),
    )
    inlines = [ProjectInline]


class ContractInline(admin.TabularInline):
    model = Contract
    extra = 0
    fields = ('title', 'client', 'start_date', 'end_date')

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    # Exibe quase todos os campos importantes na lista
    list_display = ('name', 'contract', 'status', 'expected_completion_date', 'get_thumbnail_display')
    list_filter = ('status', 'contract__architect')
    search_fields = ('name', 'contract__title')
    readonly_fields = ('conversation_log',) # Log geralmente é melhor deixar apenas leitura

    def get_thumbnail_display(self, obj):
        # Exibe uma pequena prévia se houver imagem
        if obj.get_thumbnail:
            from django.utils.html import format_html
            return format_html('<img src="{}" style="width: 45px; height: auto;" />', obj.get_thumbnail)
        return "No Image"
    get_thumbnail_display.short_description = 'Thumbnail'

@admin.register(Architect)
class ArchitectAdmin(admin.ModelAdmin):
    list_display = ('user', 'logo', 'get_role', 'firm_name', 'license_number', 'phone_number')
    fields = ('user', 'logo', 'get_role_display_only', 'firm_name', 'license_number', 'phone_number')
    search_fields = ('user__email', 'firm_name', 'license_number')
    inlines = [ContractInline]

    # fields defines what is inside the Edit/Create form
    # Note: custom methods MUST be in readonly_fields to appear here
    fields = ('user', 'logo', 'get_role_display_only', 'firm_name', 'license_number', 'phone_number')
    readonly_fields = ('get_role_display_only',)

    def get_role(self, obj):
        return obj.user.get_role_display()
    get_role.short_description = 'Papel Atual'

    def get_role_display_only(self, obj):
        return obj.user.role
    get_role_display_only.short_description = 'Role ID'

@admin.register(ClientProfile)
class ClientProfileAdmin(admin.ModelAdmin):
    # 'user__role' permite ver o papel na lista, 'user__email' identifica o usuário
    list_display = ('user_email', 'get_role', 'architect', 'company_name')
    
    # Adicionamos o campo 'role' do modelo Seller para ser editado junto com o Perfil
    fields = ('user', 'get_role_display_only', 'architect', 'company_name', 'phone_number')
    readonly_fields = ('get_role_display_only',)

    def user_email(self, obj):
        return obj.user.email
    user_email.short_description = 'Email'

    def get_role(self, obj):
        return obj.user.get_role_display()
    get_role.short_description = 'Papel Atual'

    def get_role_display_only(self, obj):
        return obj.user.role
    get_role_display_only.short_description = 'Role ID'

@admin.register(Operator)
class OperatorAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_role', 'department', 'access_level')
    fields = ('user', 'get_role_display_only', 'department', 'access_level')
    list_editable = ('access_level',) # Permite mudar o nível direto na lista
    search_fields = ('user__email', 'department')
    list_filter = ('department', 'access_level')

    # fields defines the layout of the edit form
    # Note: 'get_role_display_only' MUST be in readonly_fields to appear here
    fields = ('user', 'get_role_display_only', 'department', 'access_level')
    readonly_fields = ('get_role_display_only',)

    def get_role(self, obj):
        return obj.user.get_role_display()
    get_role.short_description = 'Papel Atual'

    def get_role_display_only(self, obj):
        return obj.user.role
    get_role_display_only.short_description = 'Role ID'