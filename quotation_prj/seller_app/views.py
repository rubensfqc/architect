from django.shortcuts import render, redirect, get_object_or_404
from quotation_app.models import Product
from quotation_app.forms import ProductForm
# accounts/views.py
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate
from django.contrib import messages
from seller_app.models import Seller
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import CustomUserCreationForm

def seller_dashboard(request):
    seller = get_object_or_404(Seller, user=request.user)  # Get logged-in seller
    products = Product.objects.filter(seller=seller)  # Filter only seller's products

    if request.method == "POST":
        form = ProductForm(request.POST, seller=seller)  # Pass seller to form
        if form.is_valid():
            form.save()
            return redirect('seller_dashboard')  # Reload page after adding a product
    else:
        form = ProductForm()

    return render(request, 'seller_app/seller_dashboard.html', {'products': products, 'form': form})


def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id, seller__user=request.user)  # Restrict deletion to seller's products
    product.delete()
    return redirect('seller_dashboard')  # Reload page after deleting


class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "seller_app/signup.html"

    def form_valid(self, form):
        response = super().form_valid(form)
        Seller.objects.create(user=self.object)  # Create a seller object after creating a user
        return response

    def form_invalid(self, form):
        response = super().form_invalid(form)   
        messages.error(self.request, "Error occurred during sign up")
        return response  # Return the response to display the error message

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('landing_page')
    else:
        form = CustomUserCreationForm()
    return render(request, 'seller_app/register.html', {'form': form})



def custom_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('landing_page')  # Change 'home' to your actual homepage URL name
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})
