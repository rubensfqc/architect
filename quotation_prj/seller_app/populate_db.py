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
    name=_("Célia Doces"),
    phone_number='1234567890',
    address='12 Av Paulista, São Paulo, SP, 01311-000 - instagram: @celia_doces',
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
    description='Design de sobrancelhas com técnicas modernas para realçar o olhar.',
    price=80,
    seller=seller
)

seller = Seller.objects.get(id=3) 
product = Product.objects.create(
    name='Vistoria de obra (por visita tecnica)',
    description='Vistoria completa de obra para garantir a qualidade e segurança da construção.',
    price=100,
    seller=seller
)
product = Product.objects.create(
    name=_("Reforma de banheiro (m², mín. 6m²)"),
    description='Reforma completa de banheiro, incluindo revestimentos, louças e acabamentos.',
    price=199.99,
    seller=seller
)
product = Product.objects.create(
    name='Reforma de cozinha (m², mín. 8m²)',
    description='Reforma completa de cozinha, incluindo armários, bancadas e revestimentos.',
    price=299.99,
    seller=seller
)

seller = Seller.objects.get(id=4)
product = Product.objects.create(
    name='Brigadeiro Gourmet (un.)',
    description='Clássico brasileiro reinventado com chocolate belga, creme de leite fresco e confeitos sofisticados como nibs de cacau ou pistache.',
    price=3.00,
    seller=seller
)
product = Product.objects.create(
    name='Camafeu de Nozes (un.)',
    description='Doce refinado feito com nozes trituradas e leite condensado, coberto com fondant branco e decorado com uma meia noz – símbolo de tradição e elegância.',
    price=3.80,
    seller=seller
)
product = Product.objects.create(
    name='Bem-Casado (min. 10, preço por un.)',
    description='Dois discos de pão de ló recheados com doce de leite e cobertos por açúcar de confeiteiro ou pasta fina. Representa a união e prosperidade dos noivos.',
    price=4.5,
    seller=seller
)
product = Product.objects.create(
    name='Tartelete de Limão (por 100g)',
    description='Mini tortinhas com base crocante, recheadas com curd de limão siciliano e finalizadas com merengue italiano tostado.',
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
    name='Mini Pavê de Nozes (por taça)',
    description='Versão em mini taças do tradicional pavê, com camadas de creme, biscoito embebido e nozes/amêndoas caramelizadas.',
    price=12.00,
    seller=seller
)

print(f"Created product: {product} --- Product ID: {product.id}") 