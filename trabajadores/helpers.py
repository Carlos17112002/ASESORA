# helpers.py
from weasyprint import HTML
from django.template.loader import render_to_string
from django.core.files.base import ContentFile
import tempfile

def generar_contrato_pdf(contrato):
    html_string = render_to_string('trabajadores/contrato_pdf.html', {'contrato': contrato})
    pdf_file = HTML(string=html_string).write_pdf()
    contrato_filename = f"contrato_{contrato.rut_trabajador}_{contrato.alias}.pdf"
    return ContentFile(pdf_file, name=contrato_filename)

# trabajadores/helpers.py
from weasyprint import HTML
from django.template.loader import render_to_string
from django.core.files.base import ContentFile

def generar_finiquito_pdf(finiquito):
    html_string = render_to_string('trabajadores/finiquito_pdf.html', {'finiquito': finiquito})
    pdf_file = HTML(string=html_string).write_pdf()
    nombre_archivo = f"finiquito_{finiquito.trabajador.rut_trabajador}_{finiquito.alias}.pdf"
    return ContentFile(pdf_file, name=nombre_archivo)


# helpers.py
from weasyprint import HTML
from django.template.loader import render_to_string
from django.core.files.base import ContentFile
from django.utils.text import slugify

def generar_liquidacion_pdf(liquidacion):
    # Preparar contexto para el template
    context = {
        'liquidacion': liquidacion,
        'trabajador': liquidacion.trabajador,
        'total_haberes': liquidacion.total_haberes(),
        'total_descuentos': liquidacion.total_descuentos(),
        'liquido_pagado': liquidacion.liquido_pagado(),
    }

    # Renderizar HTML
    html_string = render_to_string('trabajadores/liquidacion_pdf.html', context)

    # Generar PDF
    pdf_file = HTML(string=html_string).write_pdf()

    # Nombre del archivo
    rut = slugify(liquidacion.trabajador.rut_trabajador)
    alias = slugify(liquidacion.alias)
    nombre_archivo = f"liquidacion_{rut}_{liquidacion.mes}_{alias}.pdf"

    # Devolver como archivo adjunto
    return ContentFile(pdf_file, name=nombre_archivo)


def calcular_gratificacion(contrato, sueldo_minimo=529000):
    if contrato.tipo_gratificacion == 'fija':
        base = contrato.sueldo_base
        tope_mensual = (4.75 * sueldo_minimo) / 12
        monto = base * 0.25
        return int(min(monto, tope_mensual))
    else:
        return 0  # proporcional se calcula al cierre anual


def calcular_afp(nombre_afp, sueldo_base, gratificacion, bonos):
    """
    Calcula el descuento total de AFP según cotización obligatoria (10%)
    más comisión específica por AFP, aplicado sobre la remuneración imponible.
    """
    COMISIONES_AFP = {
        'uno': 0.0049,
        'modelo': 0.0058,
        'planvital': 0.0116,
        'habitat': 0.0127,
        'capital': 0.0144,
        'cuprum': 0.0144,
        'provida': 0.0145,
    }

    nombre = nombre_afp.lower()
    comision = COMISIONES_AFP.get(nombre, 0.0116)  # valor por defecto

    imponible = sueldo_base + gratificacion + bonos
    cotizacion = imponible * 0.10
    adicional = imponible * comision

    return int(cotizacion + adicional)

def calcular_salud(nombre_salud, sueldo_base, dias_trabajados, adicional_isapre=0, dias_mes=30):
    sueldo_proporcional = sueldo_base * (dias_trabajados / dias_mes)

    if nombre_salud.lower() == 'fonasa':
        return int(sueldo_proporcional * 0.07)
    elif nombre_salud.lower() == 'isapre':
        base = sueldo_proporcional * 0.07
        return int(base + adicional_isapre)
    else:
        return int(sueldo_proporcional * 0.07)  # fallback


def calcular_seguro_cesantia(tipo_contrato, sueldo_base, dias_trabajados, dias_mes=30):
    """
    Calcula el aporte del trabajador al Seguro de Cesantía según el tipo de contrato.
    El cálculo se hace sobre el sueldo proporcional a los días trabajados.
    Solo considera el descuento del trabajador (no el aporte del empleador).
    """

    sueldo_proporcional = sueldo_base * (dias_trabajados / dias_mes)

    tipo = tipo_contrato.lower()
    if tipo == 'indefinido':
        return int(sueldo_proporcional * 0.006)  # 0,6% trabajador
    elif tipo == 'plazo fijo':
        return 0  # trabajador no aporta
    elif tipo == 'casa particular':
        return 0  # trabajador no aporta
    else:
        return 0  # por defecto, sin aporte


# trabajadores/helpers.py
def calcular_liquido_pagado(liquidacion):
    # Días base del mes (puedes hacerlo dinámico si quieres)
    dias_mes = 30

    # Sueldo proporcional
    sueldo_diario = liquidacion.sueldo_base / dias_mes
    sueldo_real = sueldo_diario * liquidacion.dias_trabajados

    # Haberes
    total_haberes = sueldo_real + liquidacion.gratificacion + liquidacion.bonos

    # Descuentos previsionales
    total_descuentos = (
        liquidacion.afp +
        liquidacion.salud +
        liquidacion.seguro_cesantia +
        liquidacion.otros_descuentos
    )

    # Penalización por ausencias injustificadas
    descuento_ausente = sueldo_diario * liquidacion.dias_ausente
    total_descuentos += descuento_ausente

    # Resultado final
    liquido = total_haberes - total_descuentos
    return round(liquido)

