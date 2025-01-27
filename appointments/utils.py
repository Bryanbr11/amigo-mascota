from django.utils import timezone
from datetime import datetime, timedelta

def can_modify_appointment(appointment):
    now = timezone.now()
    appointment_datetime = timezone.make_aware(datetime.combine(appointment.fecha, appointment.hora))
    return now <= appointment_datetime - timedelta(hours=2)