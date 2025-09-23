from django.conf import settings
import os
from django.core.management import call_command

def registrar_alias(slug):
    alias = f'db_{slug}'
    ruta_db = os.path.join(settings.BASES_DIR, f'{alias}.sqlite3')

    os.makedirs(settings.BASES_DIR, exist_ok=True)
    if not os.path.exists(ruta_db):
        open(ruta_db, 'w').close()

    settings.DATABASES[alias] = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ruta_db,
        'TIME_ZONE': settings.TIME_ZONE,
        'ATOMIC_REQUESTS': False,
        'AUTOCOMMIT': True,
        'CONN_MAX_AGE': 0,
        'CONN_HEALTH_CHECKS': False,
        'OPTIONS': {},
    }

    print(f"[SSR] Alias registrado: {alias} → {ruta_db}")
    aplicar_migraciones(alias)  # ← 💡 esta línea es clave

from django.apps import apps as django_apps

def aplicar_migraciones(alias):
    for app_config in django_apps.get_app_configs():
        app_label = app_config.label
        try:
            call_command('migrate', app_label, database=alias, interactive=False, verbosity=0)
            print(f"[{alias}] ✅ Migración aplicada: {app_label}")
        except Exception as e:
            print(f"[{alias}] ❌ Error al migrar '{app_label}': {e}")
