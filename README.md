# quotation
App to Request for Quotation

Pasta principal do projeto eh a **agendME**, que contem o *settings.py* 

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

or to deactivate it is simply: `deactivate`

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
