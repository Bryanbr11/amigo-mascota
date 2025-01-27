from django.db import models
from django.conf import settings

class ActivityLog(models.Model):
    ACTION_TYPES = (
        ('CREATE', 'Creación'),
        ('UPDATE', 'Actualización'),
        ('DELETE', 'Eliminación'),
        ('LOGIN', 'Inicio de sesión'),
        ('LOGOUT', 'Cierre de sesión'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    action_type = models.CharField(max_length=20, choices=ACTION_TYPES)
    details = models.TextField()
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    content_type = models.CharField(max_length=100, blank=True, null=True)
    object_id = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        app_label = 'activity_logs'
        db_table = 'activity_logs_activitylog'
        ordering = ['-timestamp']
        verbose_name = 'Registro de actividad'
        verbose_name_plural = 'Registros de actividad'

    def __str__(self):
        return f"{self.user} - {self.action_type} - {self.timestamp}"
