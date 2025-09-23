from django.urls import path
from lecturas.views import listado_lecturas, mapa_lecturas, crear_lectura

urlpatterns = [
    path('', listado_lecturas, name='listado_lecturas'),
    path('mapa/', mapa_lecturas, name='mapa_lecturas'),
    path('crear/', crear_lectura, name='crear_lectura'),




]
