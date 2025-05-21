from django.contrib import admin
from .models import Client, Product, Quotation, QuotationProduct

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'whatsapp', 'seller')  # Fields to display in the list view
    search_fields = ('name', 'email')  # Fields to enable searching
    list_filter = ('name',)  # Fields to enable filtering

#admin.site.register(Product)
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'seller')  # Fields to display in the list view
    search_fields = ('name', 'description')
    list_filter = ('name',)

admin.site.register(Quotation)
admin.site.register(QuotationProduct)
