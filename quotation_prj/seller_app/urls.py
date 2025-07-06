from django.urls import path, include
from . import views
from .views import SignUpView

urlpatterns = [
    path('', views.seller_dashboard, name='seller_dashboard'),
    path('dashboard/', views.seller_dashboard, name='seller_dashboard'),
    path('add-product/', views.add_product, name='add_product'),
    path('edit/<int:product_id>/', views.edit_product, name='edit_product'),
    path('delete/<int:product_id>/', views.delete_product, name='delete_product'),
    path('my-quotations/', views.seller_quotations, name='seller_quotations'),
    path('update/', views.update_seller, name='update_seller'),
    path('quote-settings/', views.update_quotation_settings, name='update_quote_settings'),
    path("signup/", SignUpView.as_view(), name="signup"),
    path('register/', views.register, name='register'),
    path('clients/', views.seller_clients, name='seller_clients'),
]