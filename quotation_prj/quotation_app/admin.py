from django.contrib import admin
from .models import Client

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'whatsapp')  # Fields to display in the list view
    search_fields = ('name', 'email')  # Fields to enable searching
    list_filter = ('name',)  # Fields to enable filtering