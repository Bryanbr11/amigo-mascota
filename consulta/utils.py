from django.core.mail import send_mail
from django.conf import settings

def enviar_notificacion_consulta(consulta):
    subject = f'Consulta programada para {consulta.mascota.nombre}'
    message = f"""
    Estimado/a {consulta.mascota.propietario.get_full_name()},

    Le recordamos que tiene una consulta programada para {consulta.mascota.nombre} el día {consulta.fecha} a las {consulta.hora}.

    Motivo de la consulta: {consulta.motivo}

    Por favor, llegue 10 minutos antes de la hora programada.

    Saludos cordiales,
    El equipo veterinario
    """
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [consulta.mascota.propietario.email]
    
    send_mail(subject, message, from_email, recipient_list)

    return True 