from django.db import models
import json

class Empresa(models.Model):
    nombre = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    color_dashboard = models.CharField(max_length=20, default='#008000')
    sectores_json = models.TextField(blank=True, default='[]')  # ← lista de sectores como JSON

    def sectores(self):
        try:
            return json.loads(self.sectores_json)
        except:
            return []

    def __str__(self):
        return self.nombre

from django.db import models
from django.contrib.auth.models import User

class EliminacionEmpresa(models.Model):
    nombre = models.CharField(max_length=100)
    slug = models.CharField(max_length=50)
    ejecutado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.slug} eliminado por {self.ejecutado_por} el {self.fecha.strftime('%d/%m/%Y %H:%M')}"

