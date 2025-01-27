from django import template
from consulta.models import Consulta
from django.utils import timezone

register = template.Library()

@register.simple_tag
def get_proximas_consultas(user, limit=5):
    if user.role == 'VETERINARIAN':
        return Consulta.objects.filter(
            veterinario=user,
            fecha__gte=timezone.now().date(),
            estado='PENDIENTE'
        ).order_by('fecha', 'hora')[:limit]
    elif user.role == 'CLIENT':
        return Consulta.objects.filter(
            mascota__propietario=user,
            fecha__gte=timezone.now().date(),
            estado='PENDIENTE'
        ).order_by('fecha', 'hora')[:limit]
    return []