from seller_app.models import Seller, SellerQuotationSettings  # Adjust the import based on your app name
from quotation_app.models import Product, Client, Quotation, QuotationProduct  # Adjust the import based on your app name
from django.utils.translation import gettext_lazy as _

#First python manage.py createsuperuser
#python manage.py shell  #command used to open the django shell
#>>> exec(open('seller_app/populate_db.py').read())

# Create the Seller instance
seller = Seller.objects.create_user(
    username='plat4u',
    email='contato@plat4u.com.br',
    password='demosenha123',  # this is hashed automatically
    name='Plat4U - the Platform4yoU',
    phone_number='1234567890',
    social_media_link='https://www.instagram.com/plat4u/',
) 

seller = Seller.objects.create_user(
    username='ana',
    email='ana@exemplo.com',
    password='demosenha123',  # this is hashed automatically
    name='Ana Silva Beauty',
    phone_number='1234567890',
    social_media_link='https://www.instagram.com/ana_silva_beauty/',
    address='123 Av Vieira Souto, Rio de Janeiro, RJ, 22420-002',
) 
seller = Seller.objects.create_user(
    username='beto',
    email='beto@exemplo.com',
    password='demosenha123',  # this is hashed automatically
    name='Beto Reformas',
    phone_number='1234567890',
    social_media_link='https://www.facebook.com/beto.reformas',
    address='23 Av Delfim Moreira, Rio de Janeiro, RJ, 21420-002',
)	
seller = Seller.objects.create_user(
    username='celia',
    email='celia@exemplo.com',
    password='demosenha123',  # this is hashed automatically
    name=_("C\u00e9lia Doces"),
    phone_number='1234567890',
    social_media_link='https://www.instagram.com/celia_doces/',
    address='12 Av Paulista, S\u00e3o Paulo, SP, 01311-000',
)
print(f"Created seller: {seller} ---Seller ID: {seller.id}")


seller = Seller.objects.get(email='contato@plat4u.com.br')  # Or use id=1, etc.
quote_settings, created  = SellerQuotationSettings.objects.get_or_create(seller=seller)
quote_settings.redirect_url = "https://www.plat4u.com.br"
quote_settings.custom_message = "Para brasileiros expatriados que querem otimizar sua rotina empresarial!\n\nA Plat4U acaba de lan\u00e7ar um app inovador para facilitar sua vida: agora voc\u00ea gera cota\u00e7\u00f5es profissionais em poucos cliques, direto do seu celular!\n\nComo funciona?\n\u2022 Escolha produtos pr\u00e9-cadastrados ou personalizados para sua empresa\n\u2022 O sistema monta automaticamente um or\u00e7amento completo\n\u2022 Com sua logo, dados da empresa e visual profissional\n\nMais agilidade. Mais controle. Mais credibilidade.\n\nIdeal para quem vive fora do Brasil e precisa de solu\u00e7\u00f5es \u00e1geis, confi\u00e1veis e com suporte em portugu\u00eas.\n\nAcesse o link na bio e conhe\u00e7a o novo app da Plat4U!"
quote_settings.payment_link = "https://pay.cakto.com.br/odm4fwu_463079" 
#quote_settings.pix_key = "example@pix.com"
quote_settings.currency = "EUR"
#quote_settings.base_price = 99.90
quote_settings.save()
print(f"Created or updated quotation settings for seller: {seller.name} --- Seller ID: {seller.id}")
product = Product.objects.create(
    name='Plano de Assinatura Mensal',
    description='Assinatura mensal para acesso ilimitado ao aplicativo Plat4U, com suporte prioritário e atualizações constantes.',
    price=19.90,
    seller=seller
)
product = Product.objects.create(
    name='Plano de Assinatura Trimestral',
    description='Assinatura por trimestre para acesso ilimitado ao aplicativo Plat4U, com suporte prioritário e atualizações constantes.',
    price=49.90, #16,63 por mês
    seller=seller
)
product = Product.objects.create(
    name='Plano de Assinatura Semestral',
    description='Assinatura por seis meses para acesso ilimitado ao aplicativo Plat4U, com suporte prioritário e atualizações constantes.',
    price=89.90, #14,98 / mês
    seller=seller
)
product = Product.objects.create(
    name='Plano de Assinatura Anual',
    description='Assinatura por 12 meses para acesso ilimitado ao aplicativo Plat4U, com suporte prioritário e atualizações constantes.',
    price=169.90, #14,15 por mês
    seller=seller
)

seller = Seller.objects.get(email='ana@exemplo.com')  # Or use id=1, etc.
quote_settings, created  = SellerQuotationSettings.objects.get_or_create(seller=seller)
quote_settings.redirect_url = "https://your-redirect-url.com"
quote_settings.custom_message = "Agrade\u00e7o pela oportunidade de elaborar este or\u00e7amento para voc\u00ea! Fico \u00e0 disposi\u00e7\u00e3o para tirar qualquer d\u00favida ou ajustar detalhes conforme sua prefer\u00eancia. Aguardo seu retorno para confirmarmos o agendamento e proporcionar o melhor cuidado para sua pele."
quote_settings.payment_link = "https://your-payment-link.com"
quote_settings.pix_key = "example@pix.com"
quote_settings.currency = "BRL"
#quote_settings.base_price = 99.90
quote_settings.save()
print(f"Created or updated quotation settings for seller: {seller.name} --- Seller ID: {seller.id}")


seller = Seller.objects.get(email='beto@exemplo.com')  # Or use id=1, etc.
quote_settings, created  = SellerQuotationSettings.objects.get_or_create(seller=seller)
quote_settings.redirect_url = "https://your-redirect-url.com"
quote_settings.custom_message = "Agrade\u00e7o pela confian\u00e7a em meu trabalho! Este or\u00e7amento foi preparado com aten\u00e7\u00e3o aos detalhes da sua obra. Se precisar de ajustes ou tiver alguma d\u00favida, pode me chamar. Fico no aguardo do seu OK para fecharmos as datas e iniciarmos com tudo!"
quote_settings.payment_link = "https://your-payment-link.com"
quote_settings.pix_key = "example@pix.com"
quote_settings.currency = "CHF"
#quote_settings.base_price = 99.90
quote_settings.save()
print(f"Created or updated quotation settings for seller: {seller.name} --- Seller ID: {seller.id}")



seller = Seller.objects.get(email='celia@exemplo.com')  # Or use id=1, etc.
quote_settings, created  = SellerQuotationSettings.objects.get_or_create(seller=seller)
print(f"quote_settings 0: {quote_settings}")
quote_settings.redirect_url = "https://celia-redirect-url.com"
quote_settings.custom_message = "Muito obrigada pelo seu interesse em meus doces! Este or\u00e7amento foi feito com todo o carinho para deixar seu evento ainda mais especial. Se quiser alterar sabores, quantidades ou tirar d\u00favidas, estou \u00e0 disposi\u00e7\u00e3o. Aguardo seu retorno para fecharmos os detalhes e deixarmos tudo perfeito!"
quote_settings.payment_link = "https://celia-payment-link.com"
quote_settings.pix_key = "celia_doces@pix.com"
quote_settings.currency = "EUR"
#quote_settings.base_price = 99.90
quote_settings.save()
print(f"quote_settings 1: {quote_settings}")
print(f"Created or updated quotation settings for seller: {seller.name} --- Seller ID: {seller.id}")


seller = Seller.objects.get(email='ana@exemplo.com')  # Get the seller instance by ID
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

seller = Seller.objects.get(email='beto@exemplo.com')
product = Product.objects.create(
    name='Vistoria de obra (por visita t\u00e9cnica)',
    description='Vistoria completa de obra para garantir a qualidade e segurança da constru\u00e7\u00e3o.',
    price=100,
    seller=seller
)
product = Product.objects.create(
    name=_("Reforma de banheiro (m\u00b2, m\u00edn. 6m\u00b2)"),
    description='Reforma completa de banheiro, incluindo revestimentos, louças e acabamentos.',
    price=199.99,
    seller=seller
)
product = Product.objects.create(
    name='Reforma de cozinha (m\u00b2, m\u00edn. 8m\u00b2)',
    description='Reforma completa de cozinha, incluindo arm\u00e1rios, bancadas e revestimentos.',
    price=299.99,
    seller=seller
)

seller = Seller.objects.get(email='celia@exemplo.com')
product = Product.objects.create(
    name='Brigadeiro Gourmet (un.)',
    description='Cl\u00e1ssico brasileiro reinventado com chocolate belga, creme de leite fresco e confeitos sofisticados como nibs de cacau ou pistache.',
    price=3.00,
    seller=seller
)
product = Product.objects.create(
    name='Camafeu de Nozes (un.)',
    description='Doce refinado feito com nozes trituradas e leite condensado, coberto com fondant branco e decorado com uma meia noz, s\u00edmbolo de tradi\u00e7\u00e3o.',
    price=3.80,
    seller=seller
)
product = Product.objects.create(
    name='Bem-Casado (min. 10, pre\u00e7o por un.)',
    description='Dois discos de p\u00e3o de l\u00f3 recheados com doce de leite e cobertos por a\u00e7\u00facar de confeiteiro ou pasta fina. Representa a uni\u00e3o e prosperidade dos noivos.',
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
    name='Mini Pav\u00ea de Nozes (por ta\u00e7a)',
    description='Vers\u00e3o em mini ta\u00e7as do tradicional pav\u00ea, com camadas de creme, biscoito embebido e nozes/am\u00eandoas caramelizadas.',
    price=12.00,
    seller=seller
)

print(f"Created product: {product} --- Product ID: {product.id}") 