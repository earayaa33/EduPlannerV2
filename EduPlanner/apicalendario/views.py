from .models import Evento
import requests
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser, AllowAny
from rest_framework.response import Response
from .serializers import EventoSerializer
from rest_framework import viewsets, generics, status
from rest_framework.views import APIView
from datetime import date
from rest_framework.decorators import api_view

class EventoViewSet(viewsets.ModelViewSet):
    queryset = Evento.objects.all()
    serializer_class = EventoSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        # Obtener la fecha del evento
        fecha_evento = serializer.validated_data['fecha_inicio']
        
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
                if fecha_evento == date.fromisoformat(fecha_feriado):  # Comparamos solo la fecha
                    raise ValueError(f"No se puede crear un evento en un día feriado: {fecha_feriado}")
        else:
            # Si no se pudo obtener los feriados de la API
            raise ValueError("No se pudo obtener la lista de feriados para realizar la validación.")

        # Si no hay conflicto con los feriados, guardar el evento
        serializer.save()

    def create(self, request, *args, **kwargs):
        try:
            # Llamamos a perform_create para que se ejecute la validación
            return super().create(request, *args, **kwargs)
        except ValueError as e:
            # Si hay un error de validación (por ejemplo, fecha feriado)
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class EventosYFeriadosAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        eventos = Evento.objects.all()
        eventos_serializados = EventoSerializer(eventos, many=True).data

        url = "https://api.boostr.cl/holidays.json"

        headers = {"accept": "application/json"}

        response = requests.get(url, headers=headers)

        feriados = response.json().get("data",[])

        eventos_a_ordenar = [
            {"titulo":evento["titulo"], "descripcion":evento["descripcion"], "fecha_inicio":evento["fecha_inicio"], "fechas_finalizacion":evento["fecha_finalizacion"]}
            for evento in eventos_serializados
        ]
        feriados_a_ordenar = [
            {"titulo":feriado["title"], "fecha_inicio":feriado["date"], "tipo":feriado["type"]}
            for feriado in feriados
        ]

        eventos_combinados =  eventos_a_ordenar + feriados_a_ordenar

        for item in eventos_combinados:
            item["fecha_inicio"] = date.fromisoformat(item["fecha_inicio"])

        eventos_combinados.sort(key=lambda x: x["fecha_inicio"])

        return Response(eventos_combinados)

