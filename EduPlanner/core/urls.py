from django.urls import path
from core import views as vistas
from . import views

urlpatterns = [
    path('', vistas.inicio, name='inicio_redireccion'),
    path('inicio/', vistas.inicio, name='inicio'),
    path('Iniciar Sesion/', vistas.IniciarSesion, name='Iniciar Sesion'), 
    path('Registrarse/', vistas.Registrarse, name='Registrarse'),   
    path('salir/', vistas.salir, name='salir'),
    path('Panel Admin/', vistas.PanelAdmin, name='Panel Admin'),
    path('Modificar evento/', vistas.ModificarEvento, name='Modificar evento'),
    path('api/eventos/', views.obtener_eventos, name='obtener_eventos'),
]