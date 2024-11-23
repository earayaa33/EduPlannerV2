from .models import Evento
from rest_framework.permissions import IsAuthenticated
from .serializers import EventoSerializer
from rest_framework import viewsets

class EventoViewSet(viewsets.ModelViewSet):
    queryset = Evento.objects.all()
    serializer_class = EventoSerializer
    permission_classes = (IsAuthenticated,)
