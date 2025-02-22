from django.urls import path
from . import views

urlpatterns = [
    path('', views.email_page, name='email_page'),
    path('email-success/', views.email_success, name='email_success'),
]