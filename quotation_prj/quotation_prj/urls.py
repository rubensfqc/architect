"""
URL configuration for quotation_prj project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from quotation_app import views
from django.contrib.auth import views as auth_views
#from email_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home_view, name='home'),  # Set this as the home view
    path('lp', views.landing_page, name='landing_page'),
    path('quotation/<int:client_id>/', views.quotation_page, name='quotation_page'),
    path('add-product/', views.add_product, name='add_product_page'),
    path('generate-pdf/<int:quotation_id>/', views.generate_pdf, name='generate_pdf'),
    path('email/', include('email_app.urls')),
    path('seller/', include('seller_app.urls')),
    path('accounts/', include('django.contrib.auth.urls')), # o logout da base.html estah sendo achado por aqui
    #path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    #path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('seller/<slug:slug>/', views.landing_page_per_seller, name='landing_page_per_seller'),
    path('seller/<slug:slug>/<int:client_id>', views.quotation_page_per_seller, name='quotation_page_per_seller')
]
