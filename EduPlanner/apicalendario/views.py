from .models import Evento
from .permissions import administradorAcademico, usuarioComun
from .serializers import EventoSerializer
from rest_framework import viewsets

class EventoViewSet(viewsets.ModelViewSet):
    queryset = Evento.objects.all()
    serializer_class = EventoSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'destroy']: 
            return [administradorAcademico()]
        else:  
            return [usuarioComun()]