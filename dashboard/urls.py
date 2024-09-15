from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from dashboard import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
 path('get_images/', views.get_images, name='get_images'), 
] 