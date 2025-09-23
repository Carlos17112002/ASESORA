from django.db import models
from empresas.models import Empresa
from django.utils import timezone

class PreguntaFrecuente(models.Model):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, null=True)

    pregunta = models.CharField(max_length=200)
    respuesta = models.TextField()
    categoria = models.CharField(max_length=100, blank=True)
    activa = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.pregunta[:50]}..."
