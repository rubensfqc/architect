from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.architect_dashboard, name='architects_dashboard'),
    path('projects/', views.project_list, name='architects_projects'),
    path('clients/', views.client_list, name='architects_clients'),
    path('contracts/', views.contract_list, name='architects_contracts'),
    path('client/dashboard/', views.client_dashboard, name='client_dashboard'),
    path('contracts/add/', views.contract_upsert, name='contract_add'),
    path('contracts/edit/<int:pk>/', views.contract_upsert, name='contract_edit'),
    path('contracts/delete/<int:pk>/', views.contract_delete, name='contract_delete'),
]