from .models import Evento
import requests
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser, AllowAny
from rest_framework.response import Response
from .serializers import EventoSerializer
from rest_framework import viewsets, generics
from rest_framework.views import APIView
from datetime import date


#class EventoListAPIView(generics.ListAPIView):
   # queryset = Evento.objects.all()
    #serializer_class = EventoSerializer

#Contiene todas las opciones

#class EventoViewSet(viewsets.ModelViewSet):
   #queryset = Evento.objects.all()
   #serializer_class = EventoSerializer

#class EventoListAPIView(generics.ListAPIView):
    #queryset = Evento.objects.all()
   # serializer_class = EventoSerializer

class EventoViewSet(viewsets.ModelViewSet):
    queryset = Evento.objects.all()
    serializer_class = EventoSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

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

#class EventoDetalleAPIView(generics.RetrieveUpdateDestroyAPIView):
   # queryset = Evento.objects.all()
    #serializer_class = EventoSerializer 

   # def get_permissions(self):
        #if self.request.method in['PUT', "DELETE", 'PATCH'] :
          #  return [IsAdminUser()]
        #return [AllowAny()]