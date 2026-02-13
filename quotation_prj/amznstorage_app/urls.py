# amznstorage_app/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.document_list, name='document_list'),
    path('upload/', views.upload_document, name='upload_document'),
    path('upload/project/<int:project_id>/', views.upload_document, name='project_document_upload'),    # New route for project-specific uploads
    path('document/<int:pk>/', views.document_detail, name='document_detail'),
    path("pdf-proxy/<int:document_id>/", views.pdf_proxy, name="pdf_proxy"),
]