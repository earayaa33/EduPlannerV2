from apicalendario import views
from rest_framework import routers
from django.urls import path, include

router = routers.DefaultRouter()

#Se añaden al router los endpoints a los viewsets

router.register('eventos-publicos', views.EventosPublico, basename='eventos_publicos')
router.register('eventos', views.EventosViewSet, basename='eventos')
router.register('eventos-publicos-y-feriados', views.EventosYFeriadosPublicoViewSet, basename='eventos_publicos_y_feriados')
router.register('eventos-y-feriados', views.EventosYFeriadosViewSet, basename='eventos_y_feriados')

urlpatterns = [
    path('', include(router.urls)),
    
]
