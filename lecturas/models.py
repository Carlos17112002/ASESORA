from django.db import models

# Create your models here.
from django.db import models
from clientes.models import Cliente

class Lectura(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    fecha = models.DateField()
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    observacion = models.TextField(blank=True)
    empresa_slug = models.CharField(max_length=50, db_index=True, null=True, blank=True)

    def __str__(self):
        return f"{self.cliente.nombre} → {self.valor} kWh ({self.fecha})"
