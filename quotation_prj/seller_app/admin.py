from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Seller

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