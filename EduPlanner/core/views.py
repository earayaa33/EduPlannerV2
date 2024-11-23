from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login
from core.forms import RegistroUserCreationForm
from django.contrib.auth import authenticate

# Create your views here.
from django.http import HttpResponse

def inicio (request):
    return render(request,'core/inicio.html')

@login_required
def IniciarSesion(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('inicio') 
    return render(request, 'core/Iniciar Sesion.html')   

def salir(request):
    logout(request)
    return redirect("inicio")

def Registrarse(request):
    data = {
        'form': RegistroUserCreationForm()      
    }   

    if request.method == 'POST':
            Formulario = RegistroUserCreationForm(data=request.POST)
            if Formulario.is_valid():
                user = Formulario.save()

                usuario_autenticado = authenticate(username=Formulario.cleaned_data["username"], password=Formulario.cleaned_data["password1"])
                login(request, usuario_autenticado)
                return redirect(to='inicio')
            else:
                data['form'] = Formulario

    return render(request,'registration/Registrarse.html', data)        