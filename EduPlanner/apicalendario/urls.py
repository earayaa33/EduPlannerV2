from apicalendario import views
from rest_framework import routers
from django.urls import path, include
from .views import EventosYFeriadosAPIView

router = routers.DefaultRouter()

#Se añaden al router los endpoints a los viewsets

router.register('eventos', views.EventoViewSet, basename='evento')
router.register('eventos-por-aprobar', views.EventosPorAprobarViewSet, basename='eventos_por_aprobar')

urlpatterns = [
    path('', include(router.urls)),
    path('eventos-y-feriados/', EventosYFeriadosAPIView.as_view()),
    #path('eventos/', views.EventoListCreateAPIView.as_view()),
    #path('eventos/create', views.EventoCreateAPIView.as_view()),
    #path('eventos/<int:pk>', views.EventoDetalleAPIView.as_view())
    
]
