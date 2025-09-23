from django.urls import path
from empresas import views
from empresas.views import crear_admin_empresa, eliminar_empresa, generar_boletas_ssr, listado_empresas
from contabilidad.views import panel_libro_sii

urlpatterns = [
    path('admin_ssr/dashboard/', views.dashboard_admin_ssr, name='dashboard_admin_ssr'),
    path('admin_ssr/crear/', views.crear_empresa, name='crear_empresa'),
    path('<slug:slug>/panel_empresa/', views.panel_empresa, name='panel_empresa'),
    path('crear-admin/<slug:slug>/', crear_admin_empresa, name='crear_admin_empresa'),
    path('eliminar/<slug:slug>/', eliminar_empresa, name='eliminar_empresa'),
    path('empresas/<slug:slug>/generar-boletas/', generar_boletas_ssr, name='generar_boletas_ssr'),
    path('listado/', listado_empresas, name='listado_empresas'),
    path('contabilidad/<slug:alias>/', panel_libro_sii, name='panel_contable')


]
