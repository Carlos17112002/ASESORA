from django.contrib import admin

# Register your models here.
# boletas/admin.py
from django.contrib import admin
from .models import Boleta

@admin.register(Boleta)
class BoletaAdmin(admin.ModelAdmin):
    list_display = ['cliente', 'periodo', 'consumo', 'monto', 'pagada']
    list_filter = ['pagada', 'periodo']
    search_fields = ['cliente__nombre', 'cliente__rut']
