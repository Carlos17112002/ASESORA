from django.db import models

# Create your models here.
# clientes/models.py

from django.db import models
from django.contrib.auth.models import User
from empresas.models import Empresa

class Cliente(models.Model):
    usuario_id = models.IntegerField(null=True, blank=True)
    empresa_slug = models.CharField(max_length=50, null=True, blank=True, db_index=True)
    nombre = models.CharField(max_length=100)
    rut = models.CharField(max_length=12, unique=True)
    direccion = models.CharField(max_length=150)
    telefono = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    medidor = models.CharField(max_length=20, unique=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    sector = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f"{self.nombre} ({self.rut})"
