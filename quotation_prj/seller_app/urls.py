from django.urls import path
from . import views

urlpatterns = [
    path('', views.seller_dashboard, name='seller_dashboard'),
    path('delete/<int:product_id>/', views.delete_product, name='delete_product'),
]