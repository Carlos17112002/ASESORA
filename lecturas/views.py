from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from lecturas.models import Lectura
from empresas.models import Empresa
from clientes.models import Cliente

def listado_lecturas(request, alias):
    slug = alias
    alias_db = f'db_{slug}'
    empresa = Empresa.objects.get(slug=slug)
    sectores = empresa.sectores()

    lecturas = Lectura.objects.using(alias_db).select_related('cliente').all()

    # Filtros
    sector = request.GET.get('sector')
    fecha = request.GET.get('fecha')

    if sector:
        lecturas = lecturas.filter(cliente__sector=sector)
    if fecha:
        lecturas = lecturas.filter(fecha=fecha)

    lecturas = lecturas.order_by('-fecha')

    return render(request, 'lecturas/listado_lecturas.html', {
        'empresa': empresa,
        'slug': slug,
        'lecturas': lecturas,
        'sectores': sectores,
    })

from django.shortcuts import render
from clientes.models import Cliente
from empresas.models import Empresa

def mapa_lecturas(request, alias):
    slug = alias
    alias_db = f'db_{slug}'
    empresa = Empresa.objects.get(slug=slug)
    clientes = Cliente.objects.using(alias_db).exclude(latitude=None).exclude(longitude=None)

    return render(request, 'lecturas/mapa_lecturas.html', {
        'empresa': empresa,
        'slug': slug,
        'clientes': clientes,
    })

from django.shortcuts import redirect
from lecturas.models import Lectura
from clientes.models import Cliente

def crear_lectura(request, alias):
    if request.method == 'POST':
        alias_db = f'db_{alias}'
        cliente_id = request.POST.get('cliente_id')
        fecha = request.POST.get('fecha')
        valor = request.POST.get('valor')
        observacion = request.POST.get('observacion')

        cliente = Cliente.objects.using(alias_db).get(id=cliente_id)

        Lectura.objects.using(alias_db).create(
            cliente=cliente,
            fecha=fecha,
            valor=valor,
            observacion=observacion,
            empresa_slug=alias
        )

    return redirect('mapa_lecturas', alias=alias)


from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.utils.dateparse import parse_datetime
from django.utils import timezone
from django.contrib.auth.models import User
from lecturas.models import Lectura
from clientes.models import Cliente
import json

@csrf_exempt
def sincronizar_lecturas(request, alias):
    if request.method != 'POST':
        return JsonResponse({'error': 'Método no permitido'}, status=405)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Formato JSON inválido'}, status=400)

    recibidas = len(data)
    guardadas = 0
    errores = []

    for item in data:
        try:
            cliente = Cliente.objects.using(f'db_{alias}').get(id=item['cliente_id'])

            fecha = parse_datetime(item['fecha']) or timezone.now()
            valor = item['lectura']
            observacion = item.get('observacion', '')

            # Validación: evitar duplicados por cliente y fecha
            existe = Lectura.objects.using(f'db_{alias}').filter(
                cliente=cliente,
                fecha=fecha.date()
            ).exists()
            if existe:
                errores.append({
                    'cliente_id': item['cliente_id'],
                    'motivo': 'Lectura ya registrada para esa fecha'
                })
                continue

            Lectura.objects.using(f'db_{alias}').create(
                cliente=cliente,
                fecha=fecha.date(),
                valor=valor,
                observacion=observacion,
                empresa_slug=alias
            )
            guardadas += 1

        except Cliente.DoesNotExist:
            errores.append({
                'cliente_id': item['cliente_id'],
                'motivo': 'Cliente no encontrado'
            })
        except Exception as e:
            errores.append({
                'cliente_id': item.get('cliente_id'),
                'motivo': str(e)
            })

    return JsonResponse({
        'recibidas': recibidas,
        'guardadas': guardadas,
        'rechazadas': len(errores),
        'errores': errores
    })


