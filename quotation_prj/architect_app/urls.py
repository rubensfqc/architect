from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.architect_dashboard, name='architects_dashboard'),
    path('projects/', views.project_list, name='architects_projects'),
    path('clients/', views.client_list, name='architects_clients'),
    path('contracts/', views.contract_list, name='architects_contracts'),
    # Update other names like update_seller to update_architect if desired
]