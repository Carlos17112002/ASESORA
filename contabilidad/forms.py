from django import forms
from .models import MovimientoContable

class MovimientoForm(forms.ModelForm):
    class Meta:
        model = MovimientoContable
        fields = ['cuenta', 'fecha', 'descripcion', 'monto', 'tipo']
