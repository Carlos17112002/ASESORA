from boletas.models import Boleta
from clientes.models import Cliente
from lecturas.models import Lectura
from datetime import date

# 🧮 Tarifa escalonada por bloques
def calcular_monto_escalonado(consumo):
    bloques = [
        (10, 180),   # 1–10 m³
        (10, 315),   # 11–20
        (10, 470),   # 21–30
        (10, 840),   # 31–40
        (10, 1360),  # 41–50
        (10, 1800),  # 51–60
        (10, 2200),  # 61–70
        (429, 2300)  # 71–500
    ]

    restante = consumo
    total = 0

    for limite, precio in bloques:
        if restante <= 0:
            break
        cantidad = min(restante, limite)
        total += cantidad * precio
        restante -= cantidad

    return total

# 🧾 Generador de boletas por alias
def generar_boletas_por_alias(alias):
    alias_db = f'db_{alias}'
    hoy = date.today()
    periodo = hoy.strftime('%B %Y')

    clientes = Cliente.objects.using(alias_db).all()
    generadas = []

    for cliente in clientes:
        lecturas = Lectura.objects.using(alias_db).filter(cliente=cliente).order_by('-fecha')

        if lecturas.count() < 1:
            print(f"[Boleta] Cliente {cliente.nombre} no tiene lecturas. Saltando.")
            continue

        lectura_actual = lecturas[0]
        lectura_anterior_valor = lecturas[1].valor if lecturas.count() >= 2 else 0
        consumo = lectura_actual.valor - lectura_anterior_valor

        if consumo <= 0:
            print(f"[Boleta] Cliente {cliente.nombre} tiene consumo negativo o nulo. Saltando.")
            continue

        # Evitar duplicados
        existe = Boleta.objects.using(alias_db).filter(cliente=cliente, periodo=periodo).exists()
        if existe:
            print(f"[Boleta] Ya existe boleta para {cliente.nombre} en {periodo}. Saltando.")
            continue

        monto_variable = calcular_monto_escalonado(consumo)
        monto_total = monto_variable + 1700  # 🧱 cargo fijo

        boleta = Boleta.objects.using(alias_db).create(
            cliente=cliente,
            periodo=periodo,
            lectura_anterior=lectura_anterior_valor,
            lectura_actual=lectura_actual.valor,
            consumo=consumo,
            monto=monto_total
        )
        generadas.append(boleta)
        print(f"[Boleta] Generada para {cliente.nombre} → {consumo} m³ → ${monto_total}")

    return generadas
