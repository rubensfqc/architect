from django.shortcuts import render, redirect, get_object_or_404
from quotation_app.models import Product, Quotation
from quotation_app.forms import ProductForm
# accounts/views.py
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from seller_app.models import Seller
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import CustomUserCreationForm, SellerUpdateForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

@login_required
def seller_dashboard(request):
    # Get products for this seller
    products = Product.objects.filter(seller=request.user)
    seller = request.user

    return render(request, 'seller_app/seller_dashboard.html', {'products': products, 'seller': seller})

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

@login_required
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id, seller=request.user)  # Restrict deletion to seller's products
    product.delete()
    return redirect('seller_dashboard')  # Reload page after deleting

@login_required
def edit_product(request, product_id):
    # Fetch the product, ensuring the logged-in user is the seller
    product = get_object_or_404(Product, id=product_id, seller=request.user)

    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.seller = request.user  # Ensure the seller is set to the logged-in user
            form.save()  # Save the updated product
            return redirect('seller_dashboard')  # Redirect back to the seller's dashboard
    else:
        form = ProductForm(instance=product)  # Populate the form with the current product data

    return render(request, 'seller_app/edit_product.html', {'form': form, 'product': product})

@login_required
def seller_quotations(request):
    slug = request.user.slug
    try:
        seller = request.user

        # Get all clients of this seller
        client_ids = seller.clients.values_list('id', flat=True)

        # Get quotations for those clients
        quotations = Quotation.objects.filter(client_id__in=client_ids).prefetch_related('products', 'client')
        #quotations = Quotation.objects.filter(seller=seller).select_related('client').order_by('-date_created')
        print(f"DEBUG quotations: {quotations} details")
        
    except Seller.DoesNotExist:
        quotations = []  # Or redirect / raise error

    return render(request, 'seller_app/seller_quotations.html', {'slug':slug ,'quotations': quotations})

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



@login_required
def update_seller(request):
    seller = request.user
    if request.method == 'POST':
        form = SellerUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            # if successful:
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('update_seller')
    else:
        form = SellerUpdateForm(instance=request.user)
    return render(request, 'seller_app/update_seller.html', {'form': form, 'seller':seller})
