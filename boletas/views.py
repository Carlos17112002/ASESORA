from django.shortcuts import render

# Create your views here.
# boletas/views.py
from django.shortcuts import render, get_object_or_404
from .models import Boleta
from clientes.models import Cliente

def boletas_cliente_view(request, alias):
    alias_db = f'db_{alias}'
    cliente = get_object_or_404(Cliente.objects.using(alias_db), usuario_id=request.user.id)
    boletas = Boleta.objects.using(alias_db).filter(cliente=cliente).order_by('-fecha_emision')

    return render(request, 'boletas/panel_boletas.html', {
        'cliente': cliente,
        'boletas': boletas,
        'slug': alias,
    })

from django.shortcuts import render, get_object_or_404
from boletas.models import Boleta
from empresas.models import Empresa

def ver_boleta(request, alias, boleta_id):
    alias_db = f'db_{alias}'
    empresa = get_object_or_404(Empresa.objects.using(alias_db), slug=alias)
    boleta = get_object_or_404(Boleta.objects.using(alias_db), id=boleta_id, cliente__usuario_id=request.user.id)

    return render(request, 'boletas/ver_boleta.html', {
        'empresa': empresa,
        'boleta': boleta,
        'slug': alias,
    })


from transbank.webpay.webpay_plus.transaction import Transaction
from django.shortcuts import redirect, get_object_or_404
from boletas.models import Boleta

def pagar_boleta(request, alias, boleta_id):
    alias_db = f'db_{alias}'
    boleta = get_object_or_404(Boleta.objects.using(alias_db), id=boleta_id, cliente__usuario_id=request.user.id)

    if boleta.pagada:
        return redirect('ver_boleta', alias=alias, boleta_id=boleta.id)

    buy_order = f"boleta-{boleta.id}"
    session_id = f"cliente-{boleta.cliente.id}"
    amount = int(boleta.monto)
    return_url = request.build_absolute_uri(f"/boletas/{alias}/boleta/{boleta.id}/confirmar-pago/")

    # ✅ Configuración de Webpay
    options = WebpayOptions(
        commerce_code='597055555532',
        api_key='Your-API-Key-Here',
        integration_type=IntegrationType.TEST
    )
    transaction = Transaction(options)

    response = transaction.create(
        buy_order=buy_order,
        session_id=session_id,
        amount=amount,
        return_url=return_url
    )

    token = response['token']
    url = response['url']

    return redirect(f"{url}?token_ws={token}")


from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML
from boletas.models import Boleta
from empresas.models import Empresa

def descargar_boleta_pdf(request, alias, boleta_id):
    alias_db = f'db_{alias}'
    empresa = Empresa.objects.using(alias_db).get(slug=alias)
    boleta = Boleta.objects.using(alias_db).get(id=boleta_id, cliente__usuario_id=request.user.id)

    html_string = render_to_string('boletas/boleta_pdf.html', {
        'empresa': empresa,
        'boleta': boleta,
        'cliente': boleta.cliente,
    })

    pdf_file = HTML(string=html_string).write_pdf()

    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = f'filename=boleta_{boleta.periodo}_{boleta.cliente.nombre}.pdf'
    return response

from transbank.webpay.webpay_plus.transaction import Transaction
from django.shortcuts import redirect

def confirmar_pago(request, alias, boleta_id):
    token = request.GET.get('token_ws')
    response = Transaction.commit(token)

    if response['status'] == 'AUTHORIZED':
        alias_db = f'db_{alias}'
        boleta = Boleta.objects.using(alias_db).get(id=boleta_id)
        boleta.pagada = True
        boleta.metodo_pago = 'Webpay'
        boleta.fecha_pago = response['transaction_date']
        boleta.save(using=alias_db)

    return redirect('ver_boleta', alias=alias, boleta_id=boleta_id)
