from django.urls import path
from .views import avisos_view, avisos_activos_view, editar_aviso, eliminar_aviso

urlpatterns = [
    path('', avisos_view, name='avisos'),
     path('activos/', avisos_activos_view, name='avisos_activos'),
     path('editar/<int:aviso_id>/', editar_aviso, name='editar_aviso'),
    path('<slug:slug>/avisos/<int:aviso_id>/eliminar/', eliminar_aviso, name='eliminar_aviso')

]
