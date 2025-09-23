from django.shortcuts import render

# Create your views here.
# empresas/views.py

from django.shortcuts import render
from empresas.models import Empresa
from empresas.multiempresa import registrar_alias
from django.conf import settings
from django.contrib.auth.decorators import user_passes_test

@user_passes_test(lambda u: u.is_superuser)
def dashboard_admin_ssr(request):
    empresas = Empresa.objects.all().order_by('-fecha_creacion')
    empresas_con_estado = []

    for empresa in empresas:
        slug = empresa.slug
        registrar_alias(slug)  # registra alias si falta

        estado = {
            'base_creada': True,
            'alias_registrado': slug in [k.replace('db_', '') for k in settings.DATABASES.keys()],
            'tablas': {},  # podés agregar validaciones reales
            'columnas': {},
        }

        empresas_con_estado.append((empresa, estado))

    return render(request, 'admin_ssr/dashboard.html', {
        'empresas_con_estado': empresas_con_estado
    })
    
from clientes.models import Cliente
from lecturas.models import Lectura
from avisos.models import Aviso
from faq.models import PreguntaFrecuente  
from django.utils import timezone
  

def panel_empresa(request, slug):
    alias = f'db_{slug}'
    empresa = Empresa.objects.using(alias).get(slug=slug)

    total_clientes = Cliente.objects.using(alias).count()
    lecturas_mes = Lectura.objects.using(alias).filter(fecha__month=timezone.now().month).count()
    avisos_activos = Aviso.objects.using(alias).filter(empresa_id=empresa.id, activo=True).count()
    total_faq = PreguntaFrecuente.objects.using(alias).count()

    return render(request, 'admin_ssr/panel_empresa.html', {
        'empresa': empresa,
        'slug': slug,
        'total_clientes': total_clientes,
        'lecturas_mes': lecturas_mes,
        'avisos_activos': avisos_activos,
        'total_faq': total_faq,
    })


from django.shortcuts import render, redirect
from empresas.models import Empresa
from django.utils.text import slugify
from empresas.multiempresa import registrar_alias
from django.conf import settings
import os, json

def actualizar_alias_json():
    slugs = list(Empresa.objects.values_list('slug', flat=True))
    ruta_json = os.path.join(os.path.dirname(settings.__file__), 'empresas_alias.json')
    with open(ruta_json, 'w') as f:
        json.dump(slugs, f, indent=2)

def crear_empresa(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        slug = slugify(nombre)

        # Procesar sectores
        sectores_raw = request.POST.get('sectores', '')
        sectores = [s.strip() for s in sectores_raw.split(',') if s.strip()]

        # Crear empresa con sectores embebidos
        empresa = Empresa.objects.create(
            nombre=nombre,
            slug=slug,
            sectores_json=json.dumps(sectores)
        )

        registrar_alias(slug)
        actualizar_alias_json()

        return redirect('dashboard_admin_ssr')

    return render(request, 'admin_ssr/crear_empresa.html')



import json
import os
from django.conf import settings

def actualizar_alias_json():
    from empresas.models import Empresa
    slugs = list(Empresa.objects.values_list('slug', flat=True))
    ruta_json = os.path.join(settings.BASE_DIR, 'asesora_ssr', 'empresas_alias.json')

    with open(ruta_json, 'w') as f:
        json.dump(slugs, f, indent=2)


from django.contrib.auth.models import User

def crear_admin_empresa(request, slug):
    if request.method == 'POST' and request.user.is_superuser:
        nombre = request.POST.get('nombre')
        email = request.POST.get('email')
        password = User.objects.make_random_password()

        usuario = User.objects.create_user(username=slug, email=email, password=password)
        usuario.first_name = nombre
        usuario.save()

        # (Opcional) mostrar credenciales o enviarlas por email
        return redirect('dashboard_admin_ssr')

    return render(request, 'admin_ssr/crear_admin.html', {'slug': slug})

import os
import json
from django.conf import settings
from django.shortcuts import get_object_or_404, redirect
from django.db import connections
from empresas.models import Empresa, EliminacionEmpresa

def eliminar_empresa(request, slug):
    if request.method == 'POST' and request.user.is_superuser:
        empresa = get_object_or_404(Empresa, slug=slug)

        # 1. Cerrar conexión activa
        alias = f'db_{slug}'
        if alias in connections:
            connections[alias].close()

        # 2. Eliminar base física
        base_path = os.path.join(settings.BASES_DIR, f'{alias}.sqlite3')
        if os.path.exists(base_path):
            try:
                os.remove(base_path)
            except PermissionError:
                # Si sigue en uso, podés loguearlo o mostrar un mensaje
                pass

        # 3. Eliminar alias del JSON externo
        alias_json_path = os.path.join(settings.BASE_DIR, 'asesora_ssr', 'empresas_alias.json')
        if os.path.exists(alias_json_path):
            with open(alias_json_path, 'r') as f:
                aliases = json.load(f)
            if slug in aliases:
                aliases.remove(slug)
                with open(alias_json_path, 'w') as f:
                    json.dump(aliases, f, indent=2)

        # 4. Registrar en historial de auditoría
        EliminacionEmpresa.objects.create(
            nombre=empresa.nombre,
            slug=empresa.slug,
            ejecutado_por=request.user
        )

        # 5. Eliminar registro en modelo Empresa
        empresa.delete()

        # 6. Eliminar logs por alias
        log_path = os.path.join(settings.BASES_DIR, f'{slug}_log.txt')
        if os.path.exists(log_path):
            os.remove(log_path)

        return redirect('dashboard_admin_ssr')

from boletas.helpers import generar_boletas_por_alias
from empresas.models import Empresa
from django.contrib import messages

def generar_boletas_ssr(request, slug):
    if not request.user.is_superuser:
        return redirect('login_ssr')

    generadas_total = 0
    for empresa in Empresa.objects.all():
        boletas = generar_boletas_por_alias(empresa.slug)
        generadas_total += len(boletas)

    messages.success(request, f"✅ Se generaron {generadas_total} boletas correctamente.")
    return redirect('dashboard_admin_ssr')

# empresas/views.py
from django.http import JsonResponse
from empresas.models import Empresa

def listado_empresas(request):
    empresas = Empresa.objects.values('slug', 'nombre')
    return JsonResponse(list(empresas), safe=False)
