# quotation
App to Request for Quotation

Pasta principal do projeto eh a **agendME**, que contem o *settings.py* 

### Versions used

`>> python -c "import django; print(django.get_version())" >> 5.1.6`

`>python --version >> Python 3.13.2`

Pra rodar  
```
python manage.py runserver
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

### Websire benchmark
https://www.offri.nl/
