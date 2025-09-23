from django.db import models
from empresas.models import Empresa  # Ajustá si el modelo vive en otra app

class Aviso(models.Model):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, null=True)

    titulo = models.CharField(max_length=100)
    mensaje = models.TextField()
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.titulo} ({'Activo' if self.activo else 'Inactivo'})"
