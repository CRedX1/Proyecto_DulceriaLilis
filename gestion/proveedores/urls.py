from django.urls import path
from . import views

app_name = 'proveedores'

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('lista/', views.lista_proveedores, name='lista'),
    path('ordenes/', views.lista_ordenes, name='ordenes'),
    path('ordenes/nueva/', views.crear_orden, name='crear_orden'),
]