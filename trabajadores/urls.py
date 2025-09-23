from django.urls import path
from . import views

urlpatterns = [
    path('<str:alias>/nuevo_contrato/', views.crear_contrato, name='crear_contrato'),
    path('<str:alias>/contratos/', views.listado_contratos, name='listado_contratos'),
    path('<str:alias>/contrato/<int:id>/pdf/', views.ver_contrato_pdf, name='ver_contrato_pdf'),
    path('<str:alias>/contrato/<int:id>/editar/', views.editar_contrato, name='editar_contrato'),
    path('<str:alias>/crear_finiquito/', views.crear_finiquito, name='crear_finiquito'),
    path('<str:alias>/finiquitos/', views.listado_finiquitos, name='listado_finiquitos'),
    path('<str:alias>/finiquito/<int:id>/pdf/', views.ver_finiquito_pdf, name='ver_finiquito_pdf'),
    path('<str:alias>/liquidaciones/', views.listado_liquidaciones, name='listado_liquidaciones'),
    path('<str:alias>/crear_liquidacion/', views.crear_liquidacion, name='crear_liquidacion'),
    path('<str:alias>/liquidacion/<int:id>/pdf/', views.ver_liquidacion_pdf, name='ver_liquidacion_pdf'),

]
