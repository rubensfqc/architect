from django.urls import path, include
from . import views
from .views import SignUpView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.seller_dashboard, name='seller_dashboard'),
    path('delete/<int:product_id>/', views.delete_product, name='delete_product'),
    path("signup/", SignUpView.as_view(), name="signup"),
    path('register/', views.register, name='register'),
    path('login/', views.custom_login, name='login'),
    #path('login/', include('django.contrib.auth.urls')),
    #path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    #path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    #re_path(r'login$', LoginView.as_view(template_name="seller_app/login_form.html"), name="seller_login"),
    #re_path(r'logout$', LogoutView.as_view(), name="seller_logout") #LogoutView is a class not a method
]