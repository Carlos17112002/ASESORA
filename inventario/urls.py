from django.urls import path
from .views import inventario_view, agregar_item

urlpatterns = [
    path('', inventario_view, name='inventario'),
    path('agregar/', agregar_item, name='agregar_item'),  # ✅ sin slug adicional
]
