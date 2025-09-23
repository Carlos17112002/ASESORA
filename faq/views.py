from django.shortcuts import render
from empresas.models import Empresa
# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from .models import PreguntaFrecuente
from empresas.models import Empresa

def crear_faq_view(request, slug):
    alias = f'db_{slug}'
    empresa = get_object_or_404(Empresa.objects.using(alias), slug=slug)

    if request.method == 'POST':
        pregunta = request.POST.get('pregunta')
        respuesta = request.POST.get('respuesta')
        categoria = request.POST.get('categoria', '')
        activa = request.POST.get('activa') == 'on'

        if pregunta and respuesta:
            PreguntaFrecuente.objects.using(alias).create(
                empresa=empresa,
                pregunta=pregunta,
                respuesta=respuesta,
                categoria=categoria,
                activa=activa
            )
            return redirect('faq_listado', slug=slug)

    return render(request, 'faq/crear_faq.html', {
        'empresa': empresa,
        'slug': slug
    })



def faq_view(request, slug):
    alias = f'db_{slug}'
    empresa = Empresa.objects.using(alias).get(slug=slug)
    faqs = PreguntaFrecuente.objects.using(alias).filter(empresa_id=empresa.id, activa=True).order_by('categoria', '-fecha_creacion')

    return render(request, 'faq/faq_listado.html', {
        'empresa': empresa,
        'faqs': faqs,
        'slug': slug
    })
