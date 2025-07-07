from seller_app.models import Seller  # Adjust the import based on your app name
from quotation_app.models import Product, Client, Quotation, QuotationProduct  # Adjust the import based on your app name
from django.utils.translation import gettext_lazy as _

#First python manage.py createsuperuser
#python manage.py shell  #command used to open the django shell
#>>> exec(open('seller_app/populate_db.py').read())

# Create the Seller instance
seller = Seller.objects.create_user(
    username='ana',
    email='ana@exemplo.com',
    password='demosenha123',  # this is hashed automatically
    name='Ana Silva Beauty',
    phone_number='1234567890',
    address='123 Av Vieira Souto, Rio de Janeiro, RJ, 22420-002 - instagram: @ana_silva_beauty',
) 
seller = Seller.objects.create_user(
    username='beto',
    email='beto@exemplo.com',
    password='demosenha123',  # this is hashed automatically
    name='Beto Reformas',
    phone_number='1234567890',
    address='23 Av Delfim Moreira, Rio de Janeiro, RJ, 21420-002',
)	
seller = Seller.objects.create_user(
    username='celia',
    email='celia@exemplo.com',
    password='demosenha123',  # this is hashed automatically
    name=_("C\u00e9lia Doces"),
    phone_number='1234567890',
    address='12 Av Paulista, S\u00e3o Paulo, SP, 01311-000 - instagram: @celia_doces',
)
print(f"Created seller: {seller} ---Seller ID: {seller.id}")

seller = Seller.objects.get(id=2)  # Get the seller instance by ID
product = Product.objects.create(
    name='Consulta de todos os tipos de pele',
    description='Consulta completa para identificar o tipo de pele e recomendar os melhores produtos.',
    price=150,
    seller=seller
)
product = Product.objects.create(
    name='Peeling Facial',
    description='Tratamento de peeling facial para renovação celular e rejuvenescimento da pele.',
    price=280,
    seller=seller
)
product = Product.objects.create(
    name='Sobrancelha Design',
    description='Design de sobrancelhas com t\u00e9cnicas modernas para realçar o olhar.',
    price=80,
    seller=seller
)

seller = Seller.objects.get(id=3) 
product = Product.objects.create(
    name='Vistoria de obra (por visita t\u00e9cnica)',
    description='Vistoria completa de obra para garantir a qualidade e segurança da constru\u00e7\u00e3o.',
    price=100,
    seller=seller
)
product = Product.objects.create(
    name=_("Reforma de banheiro (m\u00b2, mín. 6m\u00b2)"),
    description='Reforma completa de banheiro, incluindo revestimentos, louças e acabamentos.',
    price=199.99,
    seller=seller
)
product = Product.objects.create(
    name='Reforma de cozinha (m\u00b2, mín. 8m\u00b2)',
    description='Reforma completa de cozinha, incluindo arm\u00e1rios, bancadas e revestimentos.',
    price=299.99,
    seller=seller
)

seller = Seller.objects.get(id=4)
product = Product.objects.create(
    name='Brigadeiro Gourmet (un.)',
    description='Cl\u00e1ssico brasileiro reinventado com chocolate belga, creme de leite fresco e confeitos sofisticados como nibs de cacau ou pistache.',
    price=3.00,
    seller=seller
)
product = Product.objects.create(
    name='Camafeu de Nozes (un.)',
    description='Doce refinado feito com nozes trituradas e leite condensado, coberto com fondant branco e decorado com uma meia noz, símbolo de tradi\u00e7\u00e3o.',
    price=3.80,
    seller=seller
)
product = Product.objects.create(
    name='Bem-Casado (min. 10, preço por un.)',
    description='Dois discos de pão de l\u00f3 recheados com doce de leite e cobertos por a\u00e7\u00facar de confeiteiro ou pasta fina. Representa a uni\u00e3o e prosperidade dos noivos.',
    price=4.5,
    seller=seller
)
product = Product.objects.create(
    name='Tartelete de Lim\u00e3o (por 100g)',
    description='Mini tortinhas com base crocante, recheadas com curd de lim\u00e3o siciliano e finalizadas com merengue italiano tostado.',
    price=8.50,
    seller=seller
)
product = Product.objects.create(
    name='Bombom de Uva (un.)',
    description='Uva fresca envolta em creme de leite condensado e coberta por chocolate nobre. Combina o frescor da fruta com a intensidade do chocolate.',
    price=9.50,
    seller=seller
)
product = Product.objects.create(
    name='Mini Pav\u00ea de Nozes (por taça)',
    description='Versão em mini taças do tradicional pav\u00ea, com camadas de creme, biscoito embebido e nozes/am\u00eandoas caramelizadas.',
    price=12.00,
    seller=seller
)

print(f"Created product: {product} --- Product ID: {product.id}") 