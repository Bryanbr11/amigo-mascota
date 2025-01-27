from django.db import models
from django.conf import settings
from mascotas.models import Mascota
from django.core.exceptions import ValidationError
from django.utils import timezone

class Mascota(models.Model):
    nombre = models.CharField(max_length=100)
    especie = models.CharField(max_length=50)
    raza = models.CharField(max_length=100, blank=True, null=True)
    fecha_nacimiento = models.DateField()
    propietario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='mascotas_app'  # Añade este related_name
    )
    propietario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='mascotas_consulta'  # Añade este related_name
    )

    def __str__(self):
        return f"{self.nombre} - {self.especie}"

class FichaMedica(models.Model):
    mascota = models.OneToOneField(Mascota, on_delete=models.CASCADE, related_name='ficha_medica')
    alergias = models.TextField(blank=True)
    condiciones_preexistentes = models.TextField(blank=True)
    peso = models.FloatField()
    ultima_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Ficha médica de {self.mascota.nombre}"

class Consulta(models.Model):
    TIPO_SERVICIO_CHOICES = [
        ('CONSULTA_GENERAL', 'Consulta General'),
        ('VACUNACION', 'Vacunación'),
        ('CIRUGIA', 'Cirugía'),
        ('EMERGENCIA', 'Emergencia'),
        ('CONTROL', 'Control'),
    ]

    ESTADO_CHOICES = [
        ('PENDIENTE', 'Pendiente'),
        ('REALIZADA', 'Realizada'),
        ('CANCELADA', 'Cancelada'),
    ]

    mascota = models.ForeignKey(Mascota, on_delete=models.CASCADE, related_name='consultas')
    veterinario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='consultas_realizadas')
    fecha = models.DateField(auto_now_add=True)
    motivo = models.TextField(blank=True, null=True)
    sintomas = models.TextField(blank=True, null=True)
    signos_clinicos = models.TextField(default="No especificado")
    peso = models.FloatField(null=True, blank=True)
    diagnostico = models.TextField(blank=True, null=True)
    diagnostico_ia = models.TextField(blank=True, null=True)
    tratamiento = models.TextField(blank=True, null=True)
    notas_adicionales = models.TextField(blank=True, null=True)
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='PENDIENTE')
    costo = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        default=0.00
    )
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)
    tipo_servicio = models.CharField(
        max_length=20,
        choices=TIPO_SERVICIO_CHOICES,
        default='CONSULTA_GENERAL'
    )
    calificacion = models.IntegerField(
        null=True,
        blank=True,
        choices=[
            (1, '1 - Muy Insatisfecho'),
            (2, '2 - Insatisfecho'),
            (3, '3 - Neutral'),
            (4, '4 - Satisfecho'),
            (5, '5 - Muy Satisfecho')
        ],
        help_text="Calificación de la consulta por parte del cliente"
    )
    comentario = models.TextField(
        blank=True,
        null=True,
        help_text="Comentarios o feedback del cliente sobre la consulta"
    )

    def __str__(self):
        return f"Consulta de {self.mascota.nombre} con {self.veterinario.get_full_name()} el {self.fecha}"

    def pertenece_a_usuario(self, user):
        return self.mascota.propietario == user

    class Meta:
        ordering = ['-fecha', '-creado_en']
        verbose_name = 'Consulta'
        verbose_name_plural = 'Consultas'

class HistorialConsulta(models.Model):
    consulta = models.ForeignKey(Consulta, on_delete=models.CASCADE, related_name='historial')
    fecha_modificacion = models.DateTimeField(auto_now_add=True)
    diagnostico_anterior = models.TextField(blank=True, null=True)
    tratamiento_anterior = models.TextField(blank=True, null=True)
    notas_adicionales_anteriores = models.TextField(blank=True, null=True)
    estado_anterior = models.CharField(max_length=10, choices=Consulta.ESTADO_CHOICES)

    def __str__(self):
        return f"Historial de consulta {self.consulta.id} - {self.fecha_modificacion}"

    class Meta:
        ordering = ['-fecha_modificacion']
        verbose_name = 'Historial de Consulta'
        verbose_name_plural = 'Historiales de Consultas'