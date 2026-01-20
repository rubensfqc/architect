from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.architect_dashboard, name='architects_dashboard'),
    path('projects/', views.project_list, name='architects_projects'),
    path('clients/', views.client_list, name='architects_clients'),
    path('contracts/', views.contract_list, name='architects_contracts'),
    #path('client/dashboard/', views.client_dashboard, name='client_dashboard'),
    path('contracts/add/', views.contract_upsert, name='contract_add'),
    path('contracts/edit/<int:pk>/', views.contract_upsert, name='contract_edit'),
    path('contracts/delete/<int:pk>/', views.contract_delete, name='contract_delete'),

    path('project/<int:pk>/', views.ProjectDetailView.as_view(), name='project-detail'),
    path('project/<int:pk>/edit/', views.ProjectUpdateView.as_view(), name='project-edit'),

    # The "Traffic Controller" - where users go right after login
    path('dashboard3roles/', views.dashboard_redirect, name='dashboard_redirect'),

    # Registration Routes
    path('signup/', views.signup_view, name='rolebased_signup'),

    # Role-Specific Dashboards
    path('portal/architect/', views.architect_dashboard, name='architect_dashboard'),
    path('portal/client/', views.client_dashboard, name='client_dashboard'),
    path('portal/operator/', views.operator_dashboard, name='operator_dashboard'),
]