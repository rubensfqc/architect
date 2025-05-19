from django.shortcuts import render, redirect, get_object_or_404
from quotation_app.models import Product
from quotation_app.forms import ProductForm
# accounts/views.py
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from seller_app.models import Seller
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

@login_required
def seller_dashboard(request):
    # Get products for this seller
    products = Product.objects.filter(seller=request.user)

    return render(request, 'seller_app/seller_dashboard.html', {'products': products})

@login_required
def add_product(request):#Product Dashboard
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user  # Set the seller to the logged-in user
            product.save()
            return redirect('seller_dashboard')  # Redirect to the seller dashboard after saving
    else:
        form = ProductForm()
    return render(request, 'seller_app/add_product.html', {'form': form})#, 'client': client}) #replace by seller


def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id, seller=request.user)  # Restrict deletion to seller's products
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