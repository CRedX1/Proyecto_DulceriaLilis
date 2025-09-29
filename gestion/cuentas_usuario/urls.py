from django.urls import path
from . import views

app_name = 'cuentas_usuario'

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('perfil/', views.perfil, name='perfil'),
]