from apicalendario import views
from rest_framework import routers
from django.urls import path, include

router = routers.DefaultRouter()

#Se añaden al router los endpoints a los viewsets

router.register('eventos', views.EventoViewSet)

urlpatterns = [
    path('', include(router.urls)),
    

]
