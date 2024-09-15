from django.contrib import admin
from django.urls import path, include
from api import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
  path('<int:greenhouse_id>/delete/', views.delete, name="delete"), 
  path('<int:greenhouse_id>/edit/', views.edit, name="edit"), 
  path('upload_image/', views.upload_images, name="upload_images")
]
