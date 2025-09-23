from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from .models import ItemInventario
from empresas.models import Empresa  # ✅ Correcto


def inventario_view(request, slug):
    empresa = get_object_or_404(Empresa, slug=slug)

    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        cantidad = request.POST.get('cantidad')
        categoria = request.POST.get('categoria')

        if nombre and cantidad:
            ItemInventario.objects.create(
                empresa=empresa,
                nombre=nombre,
                cantidad=int(cantidad),
                categoria=categoria
            )
            return redirect('inventario', slug=slug)

    items = ItemInventario.objects.filter(empresa=empresa).order_by('-fecha_creacion')

    return render(request, 'inventario/inventario.html', {
        'empresa': empresa,
        'items': items,
        'slug': slug
    })
    
from django.shortcuts import render, redirect, get_object_or_404
from empresas.models import Empresa  # Ajustá si tu modelo está en otra app
from .models import ItemInventario

def agregar_item(request, slug):
    empresa = get_object_or_404(Empresa, slug=slug)

    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        cantidad = request.POST.get('cantidad')
        categoria = request.POST.get('categoria')

        if nombre and cantidad:
            ItemInventario.objects.create(
                empresa=empresa,
                nombre=nombre,
                cantidad=int(cantidad),
                categoria=categoria
            )
        return redirect('inventario', slug=slug)

    # Si alguien accede por GET, redirigimos al inventario
    return redirect('inventario', slug=slug)
    
