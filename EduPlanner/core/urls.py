from django.urls import path
from core import views as vistas

urlpatterns = [
    path('', vistas.inicio, name='inicio'),
    path('Iniciar Sesion/', vistas.IniciarSesion, name='Iniciar Sesion'), 
    path('Registrarse/', vistas.Registrarse, name='Registrarse'),   
    
]