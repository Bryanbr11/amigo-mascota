from django.db import models
from django.conf import settings

class Recordatorio(models.Model):
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    fecha = models.DateField()
    hora = models.TimeField()
    completado = models.BooleanField(default=False)
    creado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='recordatorios'
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'recordatorio'
        verbose_name_plural = 'recordatorios'
        ordering = ['fecha', 'hora']

    def __str__(self):
        return f"{self.titulo} - {self.fecha}"
