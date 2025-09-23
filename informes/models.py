from django.db import models

class LibroContable(models.Model):
    empresa = models.ForeignKey('empresas.Empresa', on_delete=models.CASCADE)
    tipo = models.CharField(max_length=20, choices=[
        ('compras', 'Compras'),
        ('ventas', 'Ventas'),
        ('retenciones', 'Retenciones'),
    ])
    periodo = models.CharField(max_length=7)  # Ej: "2025-09"
    neto = models.DecimalField(max_digits=12, decimal_places=2)
    iva = models.DecimalField(max_digits=12, decimal_places=2)
    total = models.DecimalField(max_digits=12, decimal_places=2)
    estado = models.CharField(max_length=20, choices=[
        ('procesando', 'Procesando'),
        ('validado', 'Validado'),
        ('error', 'Error'),
    ], default='procesando')
    fecha_subida = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-periodo']
        verbose_name = 'Libro Contable'
        verbose_name_plural = 'Libros Contables'

    def __str__(self):
        return f"{self.tipo.title()} · {self.periodo}"



from django.db import models

class ContratoLaboral(models.Model):
    empresa = models.ForeignKey('empresas.Empresa', on_delete=models.CASCADE)
    trabajador = models.ForeignKey('trabajadores.Trabajador', on_delete=models.CASCADE)
    cargo = models.CharField(max_length=100)
    fecha_inicio = models.DateField()
    fecha_termino = models.DateField(null=True, blank=True)
    sueldo_base = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=20, choices=[('vigente', 'Vigente'), ('finalizado', 'Finalizado')], default='vigente')
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-fecha_inicio']
        verbose_name = 'Contrato Laboral'
        verbose_name_plural = 'Contratos Laborales'

    def __str__(self):
        return f"{self.trabajador.nombre} · {self.cargo}"
