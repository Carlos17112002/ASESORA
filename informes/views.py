from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404
from empresas.models import Empresa  # o el modelo que uses

def render_informe(request, alias, template_name):
    empresa = get_object_or_404(Empresa, slug=alias)
    return render(request, f'informes/{template_name}.html', {'empresa': empresa, 'slug': alias})

# Vistas individuales
def informe_cargo_descuento(request, alias): return render_informe(request, alias, 'informe_cargo_descuento')
def informe_cierre_caja(request, alias): return render_informe(request, alias, 'informe_cierre_caja')
def informe_convenios(request, alias): return render_informe(request, alias, 'informe_convenios')
def informe_DAES(request, alias): return render_informe(request, alias, 'informe_DAES')
def informe_deuda(request, alias): return render_informe(request, alias, 'informe_deuda')
def informe_lecturas(request, alias): return render_informe(request, alias, 'informe_lecturas')
def informe_socios(request, alias): return render_informe(request, alias, 'informe_socios')
def informe_subsidios(request, alias): return render_informe(request, alias, 'informe_subsidios')
def registro_macromedidor(request, alias): return render_informe(request, alias, 'registro_macromedidor')


from django.shortcuts import render, get_object_or_404
from empresas.models import Empresa
from informes.models import LibroContable

def informe_contabilidad(request, alias):
    slug = alias
    empresa = get_object_or_404(Empresa.objects.using(f'db_{slug}'), slug=slug)

    mes = request.GET.get('mes')
    tipo = request.GET.get('tipo')

    libros = LibroContable.objects.using(f'db_{slug}').filter(empresa=empresa)
    if mes:
        libros = libros.filter(periodo__icontains=mes)
    if tipo:
        libros = libros.filter(tipo=tipo)

    meses = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']

    return render(request, 'informes/informe_contabilidad.html', {
        'empresa': empresa,
        'slug': slug,
        'libros': libros,
        'meses': meses,
    })


from django.shortcuts import render, get_object_or_404
from empresas.models import Empresa
from trabajadores.models import Trabajador
from informes.models import ContratoLaboral

def informe_contratos(request, alias):
    slug = alias
    empresa = get_object_or_404(Empresa.objects.using(f'db_{slug}'), slug=slug)

    cargo = request.GET.get('cargo')
    estado = request.GET.get('estado')

    contratos = ContratoLaboral.objects.using(f'db_{slug}').filter(empresa=empresa)
    if cargo:
        contratos = contratos.filter(cargo=cargo)
    if estado:
        contratos = contratos.filter(estado=estado)

    cargos = ContratoLaboral.objects.using(f'db_{slug}').filter(empresa=empresa).values_list('cargo', flat=True).distinct()

    return render(request, 'informes/informe_contratos.html', {
        'empresa': empresa,
        'slug': slug,
        'contratos': contratos,
        'cargos': cargos,
    })
