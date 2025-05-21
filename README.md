# quotation
App to Request for Quotation

Pasta principal do projeto eh a **agendME**, que contem o *settings.py* 

### Versions used

`>> python -c "import django; print(django.get_version())" >> 5.1.6`

`>python --version >> Python 3.13.2`

### Pra rodar  
```
python manage.py runserver
```
### Para atualizar o banco de dados

Caso vc se depare com o erro no navegador
`Exception Value:	no such table: seller_app_seller`

É provavel que o banco de dados local db.sqlite3 esteja desatualizado. Para atualizar o DB rode os seguintes comandos:
```
python manage.py makemigrations
```
Em seguida
```
python manage.py migrate
```


Para acessar o projeto no [local server](http://127.0.0.1:8000/)

---

### Release Notes:

13-Feb-2025 Beginning

---

### Tips and tricks

Iniciando um projeto novo, eh preciso ter um VENV (copiar pasta) ou setar um novo

Activate the venv
```
source venv/bin/activate
```
or in Bash
```
C:\LocalData\quotation\quotation_prj>.\venv\Scripts\activate
````
and finally, to deactivate it is simply: `deactivate`

Comecar o projeto novo

`django-admin startproject quotation_prj`

Depois cd para a pasta do projeto e criar o app

`python manage.py startapp quotation_app`

Create the PDF Generation Page
Install reportlab for PDF Generation:

```
pip install reportlab
```

For the record, superuser created `admin:abc123`

```
python manage.py createsuperuser
```

### For security and obfuscation of tokens

`pip install python-decouple`

### For beatier forms

`pip install django-widget-tweaks`

### Websire benchmark
https://www.offri.nl/

### Built-in Authorization functionalitites

Using the URLconf defined in quotation_prj.urls, Django tried these URL patterns, in this order:

```
admin/
[name='landing_page']
quotation/<int:client_id>/ [name='quotation_page']
add-product/ [name='add_product_page']
generate-pdf/<int:quotation_id>/ [name='generate_pdf']
email/
seller/
accounts login/ [name='login']
accounts logout/ [name='logout']
accounts password_change/ [name='password_change']
accounts password_change/done/ [name='password_change_done']
accounts password_reset/ [name='password_reset']
accounts password_reset/done/ [name='password_reset_done']
accounts reset/<uidb64>/<token>/ [name='password_reset_confirm']
accounts reset/done/ [name='password_reset_complete']
The current path, accounts, didn’t match any of these.
```
The current path, accounts, didn’t match any of these.
