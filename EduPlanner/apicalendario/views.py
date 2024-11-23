from .models import Evento
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser, AllowAny
from .serializers import EventoSerializer
from rest_framework import viewsets, generics


#class EventoListAPIView(generics.ListAPIView):
   # queryset = Evento.objects.all()
    #serializer_class = EventoSerializer

#Contiene todas las opciones

#class EventoViewSet(viewsets.ModelViewSet):
   #queryset = Evento.objects.all()
   #serializer_class = EventoSerializer

class EventoListAPIView(generics.ListAPIView):
    queryset = Evento.objects.all()
    serializer_class = EventoSerializer

class EventoListCreateAPIView(generics.ListCreateAPIView):
    queryset = Evento.objects.all()
    serializer_class = EventoSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAdminUser()]
        return [AllowAny()]

class EventoDetalleAPIView(generics.RetrieveAPIView):
    queryset = Evento.objects.all()
    serializer_class = EventoSerializer 
