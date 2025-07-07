from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Seller, SellerQuotationSettings

@admin.register(Seller)
class SellerAdmin(UserAdmin):
    model = Seller
    list_display = ('email', 'username', 'name', 'slug', 'is_staff', 'is_active', 'address')
    list_filter = ('is_staff', 'is_active', 'groups')

    fieldsets = (
        (None, {'fields': ('username', 'email', 'password', 'address')}),
        ('Personal info', {'fields': ('name', 'phone_number', 'profile_picture')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'name', 'phone_number', 'profile_picture', 'address', 'is_staff', 'is_active')}
        ),
    )

    search_fields = ('email', 'username')
    ordering = ('email',)

#@admin.register(SellerQuotationSettings)
#class SellerQuotationSettingsAdmin(admin.ModelAdmin):
#    list_display = ('seller', 'currency', 'base_price', 'payment_link', 'custom_message')
#    search_fields = ('seller__name', 'seller__email')
#    list_filter = ('currency',)

class SellerQuotationSettingsInline(admin.StackedInline):
    model = SellerQuotationSettings
    can_delete = False
    verbose_name_plural = "Quotation Settings"

class CustomSellerAdmin(admin.ModelAdmin):
    inlines = (SellerQuotationSettingsInline,)
    list_display = ('email', 'name', 'phone_number')

admin.site.unregister(Seller)  # If already registered
admin.site.register(Seller, CustomSellerAdmin)