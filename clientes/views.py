from django.shortcuts import render, redirect
from clientes.models import Cliente
from empresas.models import Empresa
from django.contrib.auth.models import User, Group
from django.db import IntegrityError, transaction

def crear_cliente(request, alias):
    slug = alias
    alias_db = f'db_{slug}'
    empresa = Empresa.objects.get(slug=slug)
    sectores = empresa.sectores()
    error = None
    credenciales = None

    if request.method == 'POST':
        rut = request.POST.get('rut')
        nombre = request.POST.get('nombre')
        email = request.POST.get('email')
        direccion = request.POST.get('direccion')
        medidor = request.POST.get('medidor')
        telefono = request.POST.get('telefono')
        sector = request.POST.get('sector')
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')

        username = rut.replace('.', '').replace('-', '')

        if User.objects.filter(username=username).exists():
            error = 'Ya existe un usuario con ese RUT.'
        else:
            password = User.objects.make_random_password()

            try:
                with transaction.atomic():
                    # Crear usuario
                    usuario = User.objects.create_user(username=username, email=email, password=password)
                    usuario.first_name = nombre
                    usuario.save()

                    # Asignar al grupo "cliente"
                    grupo_cliente, _ = Group.objects.get_or_create(name='cliente')
                    usuario.groups.add(grupo_cliente)

                    # Crear cliente en base multiempresa
                    Cliente.objects.using(alias_db).create(
                        usuario_id=usuario.id,
                        empresa_slug=slug,
                        nombre=nombre,
                        rut=rut,
                        direccion=direccion,
                        medidor=medidor,
                        email=email,
                        telefono=telefono,
                        sector=sector,
                        latitude=latitude,
                        longitude=longitude,
                    )

                    credenciales = {'usuario': username, 'password': password}

            except Exception as e:
                # Rollback: eliminar usuario si falló la creación del cliente
                if User.objects.filter(username=username).exists():
                    User.objects.get(username=username).delete()
                error = f'Error al registrar el cliente: {str(e)}'

    return render(request, 'crear_cliente.html', {
        'empresa': empresa,
        'slug': slug,
        'sectores': sectores,
        'error': error,
        'credenciales': credenciales,
    })




from django.shortcuts import render, get_object_or_404
from clientes.models import Cliente
from lecturas.models import Lectura
from faq.models import PreguntaFrecuente as FAQ
from empresas.models import Empresa
from avisos.models import Aviso
from faq.models import  PreguntaFrecuente # Si tenés una app para preguntas frecuentes
from boletas.models import Boleta

def perfil_cliente_view(request, alias):
    slug = alias
    alias_db = f'db_{slug}'

    empresa = get_object_or_404(Empresa.objects.using(alias_db), slug=slug)
    cliente = get_object_or_404(Cliente.objects.using(alias_db), usuario_id=request.user.id)

    # 🧾 Lecturas recientes del cliente
    lecturas = Lectura.objects.using(alias_db).filter(cliente=cliente).order_by('-fecha')[:10]

    # 📢 Avisos activos
    avisos = Aviso.objects.using(alias_db).filter(activo=True).order_by('-fecha_creacion')
    
    boletas = Boleta.objects.using(alias_db).filter(cliente=cliente).order_by('-fecha_emision')


    # ❓ Preguntas frecuentes
    faqs = FAQ.objects.using(alias_db).all()

    return render(request, 'clientes/perfil_cliente.html', {
        'empresa': empresa,
        'cliente': cliente,
        'slug': slug,
        'lecturas': lecturas,
        'avisos': avisos,
        'faqs': faqs,
        'boletas': boletas,
    })

from django.shortcuts import render
from clientes.models import Cliente
from empresas.models import Empresa

def listado_clientes(request, alias):
    slug = alias
    alias_db = f'db_{slug}'
    empresa = Empresa.objects.get(slug=slug)
    sectores = empresa.sectores()

    clientes = Cliente.objects.using(alias_db).all()

    sector = request.GET.get('sector')
    rut = request.GET.get('rut')

    if sector:
        clientes = clientes.filter(sector=sector)
    if rut:
        clientes = clientes.filter(rut__icontains=rut)

    clientes = clientes.order_by('nombre')

    return render(request, 'listado_clientes.html', {
        'empresa': empresa,
        'slug': slug,
        'clientes': clientes,
        'sectores': sectores,
    })

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from clientes.models import Cliente

def login_cliente(request):
    if request.method == 'POST':
        rut = request.POST.get('rut')
        password = request.POST.get('password')
        alias = request.POST.get('alias')

        user = authenticate(request, username=rut, password=password)
        if user and user.groups.filter(name='cliente').exists():
            login(request, user)
            return redirect('perfil_cliente', alias=alias)
        else:
            error = "Credenciales inválidas o rol incorrecto"

    empresas = Empresa.objects.all()
    return render(request, 'clientes/login_cliente.html', locals())


# usuarios/views.py
from django.contrib.auth import logout
from django.shortcuts import redirect

def logout_view(request):
    logout(request)
    return redirect('login_ssr')

from django.http import JsonResponse
from clientes.models import Cliente

def clientes_por_alias(request, alias):
    try:
        clientes = Cliente.objects.using(f'db_{alias}').exclude(latitude=None).exclude(longitude=None)
        data = list(clientes.values('id', 'nombre', 'direccion', 'latitude', 'longitude'))
        return JsonResponse(data, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
