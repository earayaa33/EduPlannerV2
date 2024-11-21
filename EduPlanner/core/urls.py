from django.urls import path
from core import views as vistas

urlpatterns = [
    path('', vistas.inicio, name='inicio'),
    path('segunda/', vistas.segunda, name='segunda'),
    
]