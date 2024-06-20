# summarizer/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.upload_file, name='upload_file'),  # Route for rendering the upload form
    path('upload/', views.upload_file, name='upload'),  # Route for handling the form submission
]
