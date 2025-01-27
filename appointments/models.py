from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings
from mascotas.models import Mascota

User = get_user_model()

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.username}: {self.message[:50]}"

class Appointment(models.Model):
    ESTADO_CHOICES = [
        ('PENDIENTE', 'Pendiente'),
        ('CONFIRMADA', 'Confirmada'),
        ('EN_PROCESO', 'En Proceso'),
        ('COMPLETADA', 'Completada'),
        ('CANCELADA', 'Cancelada'),
        ('NO_ASISTIO', 'No Asistió'),
    ]

    mascota = models.ForeignKey(
        Mascota,
        on_delete=models.CASCADE,
        related_name='citas'
    )
    cliente = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='citas_cliente'
    )
    veterinario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='citas_veterinario'
    )
    fecha = models.DateField()
    hora = models.TimeField()
    motivo = models.TextField(blank=True)
    estado = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES,
        default='PENDIENTE'
    )
    notas = models.TextField(blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    ultima_modificacion = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-fecha', '-hora']
        verbose_name = 'cita'
        verbose_name_plural = 'citas'

    def __str__(self):
        return f"Cita de {self.mascota.nombre} con {self.veterinario.get_full_name()} - {self.fecha}"