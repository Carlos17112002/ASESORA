# empresas/apps.py

from django.apps import AppConfig
from django.conf import settings
from .multiempresa import registrar_alias
import os

class EmpresasConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'empresas'

    def ready(self):
        try:
            from empresas.models import Empresa
            slugs = Empresa.objects.values_list('slug', flat=True)
            for slug in slugs:
                registrar_alias(slug)
        except Exception as e:
            print(f"[SSR] Error al registrar alias: {e}")
