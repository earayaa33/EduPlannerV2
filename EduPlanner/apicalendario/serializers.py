from .models import Evento
from rest_framework import serializers

class EventoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evento
        fields = '__all__'

class EventoPublicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evento
        fields = ['titulo','descripcion','fecha_inicio','fecha_finalizacion','tipo']
