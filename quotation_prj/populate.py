from quotation_app.models import Product

Product.objects.create(name="Product A", price=10.99)
Product.objects.create(name="Product B", price=19.99)
Product.objects.create(name="Product C", price=29.99)