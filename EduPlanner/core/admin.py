from django.contrib import admin
from core.models import Evento

# Register your models here.

@admin.register(Evento) 
class EventoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'fecha_inicio', 'fecha_finalizacion', 'tipo') 
    search_fields = ('titulo', 'tipo')  