from .models import Evento
import requests
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser, AllowAny
from rest_framework.response import Response
from .serializers import EventoSerializer, EventoPublicoSerializer
from rest_framework import viewsets, generics, status
from rest_framework.views import APIView
from datetime import date
from rest_framework.decorators import api_view
from rest_framework.decorators import action

class EventosViewSet(viewsets.ModelViewSet):
    serializer_class = EventoSerializer

    queryset = Evento.objects.all()

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
         # Validación al crear un evento
        self.validar_feriado(serializer.validated_data['fecha_inicio'], serializer.validated_data['fecha_finalizacion'])
        # Si no hay conflicto, guardar el evento
        serializer.save()

    def perform_update(self, serializer):
        # Validación al actualizar un evento
        self.validar_feriado(serializer.validated_data['fecha_inicio'], serializer.validated_data['fecha_finalizacion'])
        # Si no hay conflicto, guardar el evento
        serializer.save()

    def validar_feriado(self, fecha_inicio, fecha_finalizacion):
        # Hacer una solicitud a la API de feriados para obtener los feriados
        feriados_url = "https://api.boostr.cl/holidays.json?country=CL&year=2024"  # Asegúrate de pasar el año y país correctamente
        headers = {"accept": "application/json"}

        # Realizar la solicitud a la API externa
        response = requests.get(feriados_url, headers=headers)

        if response.status_code == 200:
            feriados = response.json().get("data", [])

            # Verificar si la fecha del evento coincide con algún feriado
            for feriado in feriados:
                fecha_feriado = feriado.get("date")
                if (fecha_inicio == date.fromisoformat(fecha_feriado)) or (fecha_finalizacion == date.fromisoformat(fecha_feriado)):
                    raise ValueError(f"No se puede crear o modificar un evento en un día feriado: {fecha_feriado}")
        else:
            # Si no se pudo obtener los feriados de la API
            raise ValueError("No se pudo obtener la lista de feriados para realizar la validación.")

    def create(self, request, *args, **kwargs):
        try:
            # Llamamos a perform_create para que se ejecute la validación
            return super().create(request, *args, **kwargs)
        except ValueError as e:
            # Si hay un error de validación (por ejemplo, fecha feriado)
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        try:
            # Llamamos a perform_update para que se ejecute la validación
            return super().update(request, *args, **kwargs)
        except ValueError as e:
            # Si hay un error de validación (por ejemplo, fecha feriado)
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class EventosPublico(viewsets.ModelViewSet):
    serializer_class = EventoPublicoSerializer
    queryset = Evento.objects.filter(planificacion_interna=False, es_oficial=True)

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

class EventosYFeriadosViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]

    def list(self, request, *args, **kwargs):
        eventos_publicos = Evento.objects.filter(planificacion_interna=False, es_oficial=True)
        eventos_planificacion = Evento.objects.filter(planificacion_interna=True)
        eventos_todos = eventos_publicos | eventos_planificacion

        eventos_serializados = EventoSerializer(eventos_todos, many=True).data

        url = "https://api.boostr.cl/holidays.json"

        headers = {"accept": "application/json"}

        response = requests.get(url, headers=headers)

        feriados = response.json().get("data",[])

        eventos_a_ordenar = [
            {"id":evento["id"], "titulo":evento["titulo"], "descripcion":evento["descripcion"], "fecha_inicio":evento["fecha_inicio"], "fecha_finalizacion":evento["fecha_finalizacion"], "tipo":evento["tipo"], "feriado":False, "planificacion_interna": evento["planificacion_interna"]}
            for evento in eventos_serializados
        ]
        feriados_a_ordenar = [
            {"titulo":feriado["title"], "fecha_inicio":feriado["date"], "tipo":feriado["type"], "feriado":True}
            for feriado in feriados
        ]

        eventos_combinados =  eventos_a_ordenar + feriados_a_ordenar

        for item in eventos_combinados:
            item["fecha_inicio"] = date.fromisoformat(item["fecha_inicio"])

        eventos_combinados.sort(key=lambda x: x["fecha_inicio"])

        return Response(eventos_combinados)


class EventosYFeriadosPublicoViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]

    def list(self, request, *args, **kwargs):
        eventos = Evento.objects.filter(planificacion_interna=False, es_oficial=True)
        eventos_serializados = EventoPublicoSerializer(eventos, many=True).data

        url = "https://api.boostr.cl/holidays.json"

        headers = {"accept": "application/json"}

        response = requests.get(url, headers=headers)

        feriados = response.json().get("data",[])

        eventos_a_ordenar = [
            {"titulo":evento["titulo"], "descripcion":evento["descripcion"], "fecha_inicio":evento["fecha_inicio"], "fecha_finalizacion":evento["fecha_finalizacion"], "tipo":evento["tipo"], "feriado":False}
            for evento in eventos_serializados
        ]
        feriados_a_ordenar = [
            {"titulo":feriado["title"], "fecha_inicio":feriado["date"], "tipo":feriado["type"], "feriado":True}
            for feriado in feriados
        ]

        eventos_combinados =  eventos_a_ordenar + feriados_a_ordenar

        for item in eventos_combinados:
            item["fecha_inicio"] = date.fromisoformat(item["fecha_inicio"])

        eventos_combinados.sort(key=lambda x: x["fecha_inicio"])

        return Response(eventos_combinados)

class EventosPorAprobarViewSet(viewsets.ModelViewSet):
    queryset = Evento.objects.filter(es_oficial=False)
    serializer_class = EventoSerializer
    permission_classes = [IsAdminUser]

    @action(detail=True, methods=['post'])
    def approve_event(self, request, pk=None):
        evento = self.get_object()
        evento.es_oficial = True
        evento.save()
        return Response({"detail": "Evento aprobado y movido a eventos oficiales."}, status=status.HTTP_200_OK)

class EventosDePlanificacionInternaViewSet(viewsets.ModelViewSet):
    queryset = Evento.objects.filter(planificacion_interna=True)
    serializer_class = EventoSerializer
    permission_classes = [IsAdminUser]