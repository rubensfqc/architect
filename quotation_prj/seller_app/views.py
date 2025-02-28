from django.shortcuts import render, redirect, get_object_or_404
from quotation_app.models import Product
from quotation_app.forms import ProductForm

def seller_dashboard(request):
    products = Product.objects.all()

    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('seller_dashboard')  # Reload page after adding a product
    else:
        form = ProductForm()

    return render(request, 'seller_app/seller_dashboard.html', {'products': products, 'form': form})


def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.delete()
    return redirect('seller_dashboard')  # Reload page after deleting