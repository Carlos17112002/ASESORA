from django.db import models

# Create your models here.
# boletas/models.py
from django.db import models
from clientes.models import Cliente

class Boleta(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    periodo = models.CharField(max_length=20)  # Ej: "Agosto 2025"
    lectura_anterior = models.DecimalField(max_digits=10, decimal_places=2)
    lectura_actual = models.DecimalField(max_digits=10, decimal_places=2)
    consumo = models.DecimalField(max_digits=10, decimal_places=2)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    pagada = models.BooleanField(default=False)
    fecha_emision = models.DateField(auto_now_add=True)
    fecha_pago = models.DateField(null=True, blank=True)
    metodo_pago = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f"{self.periodo} - {self.cliente.nombre}"
