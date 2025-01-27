from django.db import models
from django.conf import settings
from mascotas.models import Mascota

class Cita(models.Model):
    ESTADO_CHOICES = [
        ('PENDIENTE', 'Pendiente'),
        ('EN_ESPERA', 'En Espera'),
        ('EN_PROCESO', 'En Proceso'),
        ('COMPLETADA', 'Completada'),
        ('CANCELADA', 'Cancelada'),
    ]
    
    mascota = models.ForeignKey(Mascota, on_delete=models.CASCADE, related_name='citas')
    veterinario = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='citas_veterinario'
    )
    fecha = models.DateField()
    hora = models.TimeField()
    motivo = models.TextField()
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='PENDIENTE')
    hora_llegada = models.TimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['fecha', 'hora']

    def __str__(self):
        return f"Cita {self.mascota.nombre} - {self.fecha}"

class Consulta(models.Model):
    cita = models.OneToOneField(Cita, on_delete=models.CASCADE, related_name='consulta')
    veterinario = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='consultas_veterinario'
    )
    mascota = models.ForeignKey(Mascota, on_delete=models.CASCADE, related_name='consultas')
    fecha = models.DateTimeField(auto_now_add=True)
    motivo_consulta = models.TextField()
    diagnostico = models.TextField()
    tratamiento = models.TextField()
    observaciones = models.TextField(blank=True)
    costo = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Consulta {self.mascota.nombre} - {self.fecha.date()}"

class Recordatorio(models.Model):
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    fecha = models.DateField()
    hora = models.TimeField()
    completado = models.BooleanField(default=False)
    creado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='recordatorios_usuario'
    )
    
    class Meta:
        ordering = ['fecha', 'hora']

    def __str__(self):
        return f"{self.titulo} - {self.fecha}" 