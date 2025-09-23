from django import forms
from .models import ContratoLaboral, FiniquitoLaboral, LiquidacionLaboral

class ContratoForm(forms.ModelForm):
    class Meta:
        model = ContratoLaboral
        fields = [
            'rut_trabajador', 'nombre', 'cargo',
            'jornada', 'tipo_contrato',
            'afp', 'salud',
            'sueldo_base', 'gratificacion', 'bonos',
            'fecha_inicio', 'fecha_termino'
        ]
        widgets = {
            'fecha_inicio': forms.DateInput(attrs={'type': 'date'}),
            'fecha_termino': forms.DateInput(attrs={'type': 'date'}),
            'afp': forms.Select(attrs={'class': 'w-full border px-3 py-2 rounded bg-white'}),
            'salud': forms.Select(attrs={'class': 'w-full border px-3 py-2 rounded bg-white'}),
            'jornada': forms.Select(attrs={'class': 'w-full border px-3 py-2 rounded bg-white'}),
            'tipo_contrato': forms.Select(attrs={'class': 'w-full border px-3 py-2 rounded bg-white'}),
        }

class FiniquitoForm(forms.ModelForm):
    class Meta:
        model = FiniquitoLaboral
        fields = [
            'trabajador', 'fecha_finiquito', 'motivo',
            'indemnizacion', 'vacaciones_pendientes', 'otros'
        ]
        widgets = {
            'fecha_finiquito': forms.DateInput(attrs={'type': 'date'}),
        }

class LiquidacionForm(forms.ModelForm):
    class Meta:
        model = LiquidacionLaboral
        fields = [
            'trabajador', 'mes',
            'sueldo_base', 'gratificacion', 'bonos',
            'horas_extra_50', 'horas_extra_100',
            'afp', 'salud', 'seguro_cesantia', 'otros_descuentos',
            'dias_trabajados', 'dias_licencia', 'dias_vacaciones', 'dias_ausente'
        ]

