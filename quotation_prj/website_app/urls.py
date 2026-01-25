# urls.py
from django.urls import path
from .views import home_view, pricing_view, landing # Import landing

urlpatterns = [
    path("", home_view, name="home"),
    path("get-pricing/", landing, name="landing"), # Add this line
    path("pricing/", pricing_view, name="pricing"),
]