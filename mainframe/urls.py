from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from pages import views as page_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', page_views.home, name='home'),
    path('pages/', include('pages.urls')),
    path('dashboard/', include('dashboard.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)