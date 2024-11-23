from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login


# Create your views here.
from django.http import HttpResponse

def inicio (request):
    return render(request,'core/inicio.html')

@login_required
def IniciarSesion(request):
    return render(request, 'core/Iniciar Sesion.html')   

def Registrarse(request):
    return render(request,'registration/Registrarse.html')      