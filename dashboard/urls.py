from django.contrib import admin
from django.urls import path, include
from dashboard import views as page_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', page_views.dashboard, name='dashboard'),
    path('greenhouses/', page_views.greenhouses, name='greenhouses'),
    path('login/', page_views.user_login, name='login'),
    path('monitoring/', page_views.monitoring, name='monitoring'),
    path('signup/', page_views.signup, name='signup'),
    path('logout/', page_views.logout, name='logout'),
    path('get_greenhouse_data/', page_views.get_greenhouse_data, name='get_greenhouse_data'),
]
