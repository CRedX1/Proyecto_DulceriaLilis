from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'cuentas_usuario'

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('login/', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('registro/', views.registro_cliente, name='registro'),
    path('dashboard-cliente/', views.dashboard_cliente, name='dashboard_cliente'),
    path('dashboard-admin/', views.dashboard_admin, name='dashboard_admin'),
    path('crear-orden/', views.crear_orden_cliente, name='crear_orden'),
]