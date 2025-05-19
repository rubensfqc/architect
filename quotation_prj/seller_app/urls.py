from django.urls import path, include
from . import views
from .views import SignUpView

urlpatterns = [
    #path('', views.seller_dashboard, name='seller_dashboard'),
    path('dashboard/', views.seller_dashboard, name='seller_dashboard'),
    path('delete/<int:product_id>/', views.delete_product, name='delete_product'),
    path("signup/", SignUpView.as_view(), name="signup"),
    path('register/', views.register, name='register'),
]