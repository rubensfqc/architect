from django.shortcuts import render, redirect
from datetime import datetime

def home_view(request):
    return render(request, "website_app/home.html", {
        "company_name": "wiserarch",
        "tagline": "Architecture is about design, not endless whatsApps and emails.",
        "year": datetime.now().year,
    })

def landing(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        whatsapp = request.POST.get("whatsapp")

        # TODO: save to DB, send email, or push to CRM
        request.session["lead"] = {
            "name": name,
            "email": email,
            "whatsapp": whatsapp,
        }

        return redirect("pricing")

    return render(request, "website_app/landing.html")


def pricing_view(request):
    if "lead" not in request.session:
        return redirect("landing")

    return render(request, "website_app/pricing.html")
