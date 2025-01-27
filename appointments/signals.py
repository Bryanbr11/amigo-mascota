from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import Appointment

@receiver(post_save, sender=Appointment)
def notify_appointment_change(sender, instance, created, **kwargs):
    subject = 'Actualización de Cita Veterinaria'
    if created:
        message = f'Se ha creado una nueva cita para {instance.mascota.nombre} el {instance.fecha} a las {instance.hora}.'
    else:
        message = f'La cita para {instance.mascota.nombre} del {instance.fecha} a las {instance.hora} ha sido actualizada. Estado actual: {instance.get_estado_display()}.'
    
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [instance.cliente.email, instance.veterinario.email],
        fail_silently=False,
    )