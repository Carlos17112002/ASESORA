from django.shortcuts import render

# Create your views here.
# views.py
from django.shortcuts import render, redirect
from .models import ContratoLaboral
from .forms import ContratoForm
from .helpers import generar_contrato_pdf

def crear_contrato(request, alias):
    if request.method == 'POST':
        form = ContratoForm(request.POST)
        if form.is_valid():
            contrato = form.save(commit=False)
            contrato.alias = alias
            contrato.save()
            contrato.documento_pdf = generar_contrato_pdf(contrato)
            contrato.save()
            return redirect(f'/trabajadores/{alias}/contratos/')
    else:
        form = ContratoForm()
    return render(request, 'trabajadores/crear_contrato.html', {'form': form, 'alias': alias})

# views.py
from django.shortcuts import render
from .models import ContratoLaboral

def listado_contratos(request, alias):
    contratos = ContratoLaboral.objects.filter(alias=alias).order_by('-creado')
    return render(request, 'trabajadores/listado_contratos.html', {
        'contratos': contratos,
        'alias': alias
    })

# views.py
from django.http import FileResponse, Http404
from .models import ContratoLaboral

def ver_contrato_pdf(request, alias, id):
    try:
        contrato = ContratoLaboral.objects.get(id=id, alias=alias)
        if contrato.documento_pdf:
            return FileResponse(contrato.documento_pdf.open(), content_type='application/pdf')
        else:
            raise Http404("Contrato sin PDF generado.")
    except ContratoLaboral.DoesNotExist:
        raise Http404("Contrato no encontrado.")

# views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import ContratoLaboral
from .forms import ContratoForm

def editar_contrato(request, alias, id):
    contrato = get_object_or_404(ContratoLaboral, id=id, alias=alias)
    if request.method == 'POST':
        form = ContratoForm(request.POST, instance=contrato)
        if form.is_valid():
            form.save()
            return redirect(f'/trabajadores/{alias}/contratos/')
    else:
        form = ContratoForm(instance=contrato)
    return render(request, 'trabajadores/editar_contrato.html', {
        'form': form,
        'alias': alias,
        'contrato': contrato
    })

from .models import FiniquitoLaboral
from .forms import FiniquitoForm
from .helpers import generar_finiquito_pdf

def crear_finiquito(request, alias):
    if request.method == 'POST':
        form = FiniquitoForm(request.POST)
        if form.is_valid():
            finiquito = form.save(commit=False)
            finiquito.alias = alias
            finiquito.save()
            finiquito.documento_pdf = generar_finiquito_pdf(finiquito)
            finiquito.save()
            return redirect(f'/trabajadores/{alias}/finiquitos/')
    else:
        form = FiniquitoForm()
    return render(request, 'trabajadores/crear_finiquito.html', {
        'form': form,
        'alias': alias
    })

def listado_finiquitos(request, alias):
    finiquitos = FiniquitoLaboral.objects.filter(alias=alias).order_by('-fecha_finiquito')
    return render(request, 'trabajadores/listado_finiquitos.html', {
        'finiquitos': finiquitos,
        'alias': alias
    })

from django.http import FileResponse, Http404
from .models import FiniquitoLaboral

def ver_finiquito_pdf(request, alias, id):
    try:
        finiquito = FiniquitoLaboral.objects.get(id=id, alias=alias)
        if finiquito.documento_pdf:
            return FileResponse(finiquito.documento_pdf.open(), content_type='application/pdf')
        else:
            raise Http404("Finiquito sin PDF generado.")
    except FiniquitoLaboral.DoesNotExist:
        raise Http404("Finiquito no encontrado.")

# trabajadores/views.py
from django.shortcuts import render, redirect
from .models import LiquidacionLaboral, ContratoLaboral
from .forms import LiquidacionForm
from .helpers import (
    generar_liquidacion_pdf,
    calcular_gratificacion,
    calcular_afp,
    calcular_salud,
    calcular_seguro_cesantia
)

COMISIONES_AFP = {
        'uno': 0.0049,
        'modelo': 0.0058,
        'planvital': 0.0116,
        'habitat': 0.0127,
        'capital': 0.0144,
        'cuprum': 0.0144,
        'provida': 0.0145,
    }

def crear_liquidacion(request, alias):
    modo = request.POST.get('modo', '')
    form_carga = LiquidacionForm()
    form_liquidacion = None
    afp_nombre = 'planvital'  # valor por defecto

    if request.method == 'POST':
        if modo == 'cargar':
            trabajador_id = request.POST.get('trabajador')
            contrato = ContratoLaboral.objects.filter(
                id=trabajador_id,
                alias=alias,
                fecha_termino__isnull=True
            ).first()

            if contrato:
                sueldo_base = contrato.sueldo_base
                gratificacion = calcular_gratificacion(contrato)
                bonos = contrato.bonos
                afp_nombre = contrato.afp.lower()
                adicional_isapre = getattr(contrato, 'plan_isapre', 0)

                initial = {
                    'trabajador': contrato.id,
                    'sueldo_base': sueldo_base,
                    'gratificacion': gratificacion,
                    'bonos': bonos,
                    'afp': calcular_afp(afp_nombre, sueldo_base, gratificacion, bonos),
                    'salud': calcular_salud(contrato.salud, sueldo_base, 30, adicional_isapre),
                    'seguro_cesantia': calcular_seguro_cesantia(contrato.tipo_contrato, sueldo_base, 30),
                    'otros_descuentos': 0,
                    'dias_trabajados': 30,
                    'dias_licencia': 0,
                    'dias_vacaciones': 0,
                    'dias_ausente': 0,
                    'horas_extra_50': 0,
                    'horas_extra_100': 0,
                }
                form_liquidacion = LiquidacionForm(initial=initial)

        elif modo == 'guardar':
            form_liquidacion = LiquidacionForm(request.POST)
            if form_liquidacion.is_valid():
                liquidacion = form_liquidacion.save(commit=False)
                liquidacion.alias = alias
                liquidacion.documento_pdf = generar_liquidacion_pdf(liquidacion)
                liquidacion.save()
                return redirect(f'/trabajadores/{alias}/liquidaciones/')

    if form_liquidacion is None:
        form_liquidacion = LiquidacionForm()

    return render(request, 'trabajadores/crear_liquidacion.html', {
        'form_carga': form_carga,
        'form_liquidacion': form_liquidacion,
        'alias': alias,
        'afp_nombre': afp_nombre,
        
    })



# views.py
from .models import LiquidacionLaboral, ContratoLaboral

def listado_liquidaciones(request, alias):
    mes = request.GET.get('mes')
    trabajador_id = request.GET.get('trabajador')

    liquidaciones = LiquidacionLaboral.objects.filter(alias=alias)
    if mes:
        liquidaciones = liquidaciones.filter(mes=mes)
    if trabajador_id:
        liquidaciones = liquidaciones.filter(trabajador_id=trabajador_id)

    trabajadores = ContratoLaboral.objects.filter(alias=alias)

    return render(request, 'trabajadores/listado_liquidaciones.html', {
        'liquidaciones': liquidaciones.order_by('-mes'),
        'trabajadores': trabajadores,
        'filtro_mes': mes,
        'filtro_trabajador': trabajador_id,
        'alias': alias
    })


from django.http import FileResponse, Http404
from .models import LiquidacionLaboral

def ver_liquidacion_pdf(request, alias, id):
    liquidacion = get_object_or_404(LiquidacionLaboral, id=id, alias=alias)
    if liquidacion.documento_pdf:
        return FileResponse(liquidacion.documento_pdf.open(), content_type='application/pdf')
    raise Http404("Liquidación sin PDF generado.")
