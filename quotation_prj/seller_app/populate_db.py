from seller_app.models import Seller  # Adjust the import based on your app name
from quotation_app.models import Product, Client, Quotation, QuotationProduct  # Adjust the import based on your app name

#python manage.py shell  #command used to open the django shell
#>>> exec(open('seller_app/populate_db.py').read())

# Create the Seller instance
seller = Seller.objects.create_user(
    username='ana',
    email='ana@example.com',
    password='securepassword123',  # this is hashed automatically
    name='Ana Silva',
    phone_number='1234567890'
)
seller = Seller.objects.create_user(
    username='bia',
    email='bia@example.com',
    password='securepassword123',  # this is hashed automatically
    name='Bia Antunes',
    phone_number='1234567890'
)
seller = Seller.objects.create_user(
    username='caio',
    email='caio@example.com',
    password='securepassword123',  # this is hashed automatically
    name='Caio Pereira',
    phone_number='1234567890'
)
print(f"Created seller: {seller} ---Seller ID: {seller.id}")

seller = Seller.objects.get(id=1) 
product = Product.objects.create(
    name='Test Product 1',
    description='This is a sample product.',
    price=49.99,
    seller=seller
)
product = Product.objects.create(
    name='Test Product 2',
    description='This is a sample product.',
    price=19.99,
    seller=seller
)

seller = Seller.objects.get(id=2) 
product = Product.objects.create(
    name='Test Product A',
    description='This is a sample product.',
    price=49.99,
    seller=seller
)
product = Product.objects.create(
    name='Test Product B',
    description='This is a sample product.',
    price=29.99,
    seller=seller
)
product = Product.objects.create(
    name='Test Product C',
    description='This is a sample product.',
    price=9.99,
    seller=seller
)

product = Product.objects.create(
    name='Test Product D',
    description='This is a sample product.',
    price=99.99,
    seller=seller
)

product = Product.objects.create(
    name='Test Product E',
    description='This is a sample product.',
    price=1.99,
    seller=seller
)
print(f"Created product: {product} --- Product ID: {product.id}")