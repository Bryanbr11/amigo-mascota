from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Consulta, HistorialConsulta

@receiver(pre_save, sender=Consulta)
def crear_historial_consulta(sender, instance, **kwargs):
    if instance.id:
        try:
            old_instance = Consulta.objects.get(id=instance.id)
            if (old_instance.diagnostico != instance.diagnostico or
                old_instance.tratamiento != instance.tratamiento or
                old_instance.notas_adicionales != instance.notas_adicionales or
                old_instance.estado != instance.estado):
                HistorialConsulta.objects.create(
                    consulta=instance,
                    diagnostico_anterior=old_instance.diagnostico,
                    tratamiento_anterior=old_instance.tratamiento,
                    notas_adicionales_anteriores=old_instance.notas_adicionales,
                    estado_anterior=old_instance.estado
                )
        except Consulta.DoesNotExist:
            pass

    if not instance.id:
        HistorialConsulta.objects.create(
            consulta=instance,
            diagnostico_anterior=None,
            tratamiento_anterior=None,
            notas_adicionales_anteriores=None,
            estado_anterior=None
        )

    instance.save()

    return old_instance
