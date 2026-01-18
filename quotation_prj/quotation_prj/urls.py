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
from django.conf.urls.static import static
from quotation_prj import settings
from seller_app import views as seller_views
#from email_app import views
from architect_app.views import architect_dashboard

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home_view, name='pages'),  # Set this as the home view
    path('search', seller_views.slug_search, name='slug_search'),  # Search by slug
    path('autocomplete/', seller_views.slug_autocomplete, name='slug_autocomplete'), 
    path('lp', views.landing_page, name='landing_page'),
    path('quotation/<int:client_id>/', views.quotation_page, name='quotation_page'),
    #path('generate-pdf/<int:quotation_id>/', views.generate_pdf, name='generate_pdf'),
    path('email/', include('email_app.urls')),
    path('pro/', include('seller_app.urls')),
    path('accounts/', include('django.contrib.auth.urls')), # o logout da base.html estah sendo achado por aqui
    #path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    #path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('pro/<slug:slug>/', views.landing_page_per_seller, name='landing_page_per_seller'),
    path('pro/<slug:slug>/<int:client_id>', views.quotation_page_per_seller, name='quotation_page_per_seller'),
    path('pro/<slug:slug>/<int:quotation_id>/', views.generate_pdf, name='generate_pdf'),
    path('arch/', include('architect_app.urls')),
    path('amzn/', include('amznstorage_app.urls')),  # Include URLs for amznstorage_app
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

