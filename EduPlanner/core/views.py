from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login
from core.forms import RegistroUserCreationForm, EventoForm 
from django.contrib.auth import authenticate

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from core.models import Evento
from core.serializers import EventoSerializer

# Create your views here.
from django.http import HttpResponse

def inicio (request):
    return render(request,'core/inicio.html')

def PanelAdmin (request):
    if request.method == 'POST':
        form = EventoForm(request.POST)
        if form.is_valid():
            # Este código será movido a una llamada a la API desde el frontend
            event_data = form.cleaned_data
            return JsonResponse({"message": "Formulario válido. Se enviará a la API."})
    else:
        form = EventoForm()
    return render(request, 'core/Panel Admin.html', {'form': form})

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
    return render(request,'registration/Registrarse.html')      
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

def ModificarEvento(request):
    return render(request, 'core/Modificar evento.html')      
    return render(request,'registration/Registrarse.html', data)        


@api_view(['GET'])
def obtener_eventos(request):
    eventos = Evento.objects.all()
    serializer = EventoSerializer(eventos, many=True)
    return Response(serializer.data)
