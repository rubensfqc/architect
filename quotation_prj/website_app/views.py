from django.shortcuts import render
from datetime import datetime

def home_view(request):
    return render(request, "website_app/home.html", {
        "company_name": "wiserArch",
        "tagline": "Spend your time wisely with your design, let us handle the clients and contracts.",
        "year": datetime.now().year,
    })
