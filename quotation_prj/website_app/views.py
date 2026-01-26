# quotation_prj/website_app/views.py
from django.shortcuts import render, redirect
from datetime import datetime
from quotation_app.forms import ClientForm
from seller_app.models import Seller

def home_view(request):
    return render(request, "website_app/home.html", {
        "company_name": "wiserarch",
        "tagline": "Architecture is about design, not endless whatsApps and emails.",
        "year": datetime.now().year,
    })

def landing(request):
    if request.method == "POST":
        form = ClientForm(request.POST)
        if form.is_valid():
            # 1. Create client instance but don't save to DB yet
            client = form.save(commit=False)
            
            # 1. Attempt to find the specific seller by email
            # 2. Fall back to the seller with ID=1 if not found
            seller = Seller.objects.filter(email="wiserarch@gmail.com").first()

            if not seller:
                try:
                    seller = Seller.objects.get(id=1)
                except Seller.DoesNotExist:
                    # Optional: Handle the rare case where even ID=1 doesn't exist
                    seller = None 

            # 3. Assign the seller to the client before saving
            client.seller = seller
            client.save()

            # 4. Keep data in session for the pricing page if needed
            request.session["lead"] = {
                "name": client.name,
                "email": client.email,
                "whatsapp": client.whatsapp,
                "client_id": client.id, # Useful for linking to quotes later
            }
            return redirect("pricing")
    else:
        form = ClientForm()

    return render(request, "website_app/landing.html", {"form": form})


def pricing_view(request):
    if "lead" not in request.session:
        return redirect("landing")

    return render(request, "website_app/pricing.html")
