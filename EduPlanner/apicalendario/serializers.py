from .models import Evento
from rest_framework import serializers

class EventoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evento
        fields = '__all__'

    def create(self, validated_data):
        es_oficial = validated_data.get('es_oficial', False)

        
        if es_oficial:
            return super().create(validated_data)
        else:
            
            evento = super().create(validated_data)
            return evento