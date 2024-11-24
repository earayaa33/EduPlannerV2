from apicalendario import views
from rest_framework import routers
from django.urls import path, include

router = routers.DefaultRouter()



router.register('eventos-publicos', views.EventosPublico, basename='eventos_publicos')
router.register('eventos', views.EventosViewSet, basename='eventos')
router.register('eventos-publicos-y-feriados', views.EventosYFeriadosPublicoViewSet, basename='eventos_publicos_y_feriados')
router.register('eventos-y-feriados', views.EventosYFeriadosViewSet, basename='eventos_y_feriados')
router.register('eventos-por-aprobar', views.EventosPorAprobarViewSet, basename='eventos_por_aprobar')
router.register('eventos-de-planificacion-interna', views.EventosDePlanificacionInternaViewSet, basename='eventos_de_planificacion_interna')


urlpatterns = [
    path('', include(router.urls)),
    
]
