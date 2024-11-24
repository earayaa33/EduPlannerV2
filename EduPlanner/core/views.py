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
from django.http import JsonResponse, HttpResponse

# Create your views here.
from django.http import HttpResponse

def inicio (request):
    return render(request,'core/inicio.html')

def PanelAdmin (request):
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
    
    TIPO_CHOICES = [
        ('inicio de semestre', 'Inicio de semestre'),
        ('fin de Semestre', 'Fin de Semestre'),
        ('inicio de Inscripción de Asignaturas','Inicio de Inscripción de Asignaturas'),
        ('fin de Inscripción de Asignaturas','Fin de Inscripción de Asignaturas'),
        ('receso Académico','Receso Académico'),
        ('feriado Nacional', 'Feriado Nacional'),
        ('feriado Regional','Feriado Regional'),
        ('inicio de Plazos de Solicitudes Administrativas','Inicio de Plazos de Solicitudes Administrativas'),
        ('fin de Plazos de Solicitudes Administrativas','Fin de Plazos de Solicitudes Administrativas'),
        ('inicio de Plazos para la Gestión de Beneficios','Inicio de Plazos para la Gestión de Beneficios'),
        ('fin de Plazos para la Gestión de Beneficios','Fin de Plazos para la Gestión de Beneficios'),
        ('ceremonia de Titulación o Graduación','Ceremonia de Titulación o Graduación'),
        ('reunión de Consejo Académico','Reunión de Consejo Académico'),
        ('talleres y Charlas','Talleres y Charlas'),
        ('día de Orientación para Nuevos Estudiantes','Día de Orientación para Nuevos Estudiantes'),
        ('eventos Extracurriculares','Eventos Extracurriculares'),
        ('inicio de Clases', 'Inicio de Clases'),
        ('ultimo Día de Clases','Último Día de Clases'),
        ('día de Puertas Abiertas','Día de Puertas Abiertas'),
        ('suspensión de Actividades Completa','Suspensión de Actividades Completa'),
        ('suspensión de Actividades Parcial','Suspensión de Actividades Parcial')


    ]


    return render(request, 'core/Modificar evento.html', {'tipo_choices': TIPO_CHOICES})      
          


@api_view(['GET'])
def obtener_eventos(request):
    eventos = Evento.objects.all()
    serializer = EventoSerializer(eventos, many=True)
    return Response(serializer.data)
