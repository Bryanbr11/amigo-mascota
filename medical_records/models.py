from django.db import models
from django.contrib.auth import get_user_model
from mascotas.models import Mascota

User = get_user_model()

class FichaMedica(models.Model):
    ESTADO_CHOICES = [
        ('ACTIVO', 'Activo'),
        ('INACTIVO', 'Inactivo'),
        ('SEGUIMIENTO', 'En Seguimiento'),
    ]

    mascota = models.ForeignKey(Mascota, on_delete=models.CASCADE, related_name='fichas_medicas')
    veterinario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='fichas_medicas_creadas')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_ultima_actualizacion = models.DateTimeField(auto_now=True)
    
    # Información médica
    peso = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text='Peso en kg')
    temperatura = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True, help_text='Temperatura corporal')
    
    # Historial médico
    diagnostico_previo = models.TextField(blank=True, null=True)
    tratamientos_anteriores = models.TextField(blank=True, null=True)
    
    # Observaciones actuales
    motivo_consulta = models.TextField()
    sintomas = models.TextField()
    diagnostico_actual = models.TextField()
    tratamiento_recomendado = models.TextField()
    
    # Estado de la ficha
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='ACTIVO')
    
    # Seguimiento
    proxima_consulta = models.DateField(null=True, blank=True)
    
    # Medicamentos
    medicamentos = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"Ficha Médica - {self.mascota.nombre} - {self.fecha_creacion.strftime('%d/%m/%Y')}"
    
    class Meta:
        verbose_name = 'Ficha Médica'
        verbose_name_plural = 'Fichas Médicas'
        ordering = ['-fecha_creacion']
