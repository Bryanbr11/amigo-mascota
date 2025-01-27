from celery import shared_task
from django.utils import timezone
from django.contrib.auth import get_user_model
from .models import Appointment
from django.core.mail import send_mail

User = get_user_model()

@shared_task
def enviar_recordatorios_citas():
    # Buscar citas en las próximas 24 horas
    citas_proximas = Appointment.objects.filter(
        fecha=timezone.now().date() + timezone.timedelta(days=1),
        estado='PENDIENTE'
    )

    for cita in citas_proximas:
        # Enviar notificación por email
        send_mail(
            'Recordatorio de Cita',
            f'Tienes una cita mañana a las {cita.hora} con {cita.veterinario}.',
            'from@example.com',
            [cita.cliente.email],
            fail_silently=False,
        )

        # Crear notificación en la plataforma
        Notification.objects.create(
            user=cita.cliente,
            message=f'Recordatorio: Tienes una cita mañana a las {cita.hora}.'
        )

    return f'Enviados {citas_proximas.count()} recordatorios.'