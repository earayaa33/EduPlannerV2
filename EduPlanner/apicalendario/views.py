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

#class EventoDetalleAPIView(generics.RetrieveUpdateDestroyAPIView):
   # queryset = Evento.objects.all()
    #serializer_class = EventoSerializer 

   # def get_permissions(self):
        #if self.request.method in['PUT', "DELETE", 'PATCH'] :
          #  return [IsAdminUser()]
        #return [AllowAny()]