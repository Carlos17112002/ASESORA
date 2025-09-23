from django.urls import path
from . import views

urlpatterns = [
    path('<slug:alias>/cargo-descuento/', views.informe_cargo_descuento, name='informe_cargo_descuento'),
    path('<slug:alias>/cierre-caja/', views.informe_cierre_caja, name='informe_cierre_caja'),
    path('<slug:alias>/contabilidad/', views.informe_contabilidad, name='informe_contabilidad'),
    path('<slug:alias>/contratos/', views.informe_contratos, name='informe_contratos'),
    path('<slug:alias>/convenios/', views.informe_convenios, name='informe_convenios'),
    path('<slug:alias>/daes/', views.informe_DAES, name='informe_DAES'),
    path('<slug:alias>/deuda/', views.informe_deuda, name='informe_deuda'),
    path('<slug:alias>/lecturas/', views.informe_lecturas, name='informe_lecturas'),
    path('<slug:alias>/socios/', views.informe_socios, name='informe_socios'),
    path('<slug:alias>/subsidios/', views.informe_subsidios, name='informe_subsidios'),
    path('<slug:alias>/macromedidor/', views.registro_macromedidor, name='registro_macromedidor'),
]
