from django.utils import timezone
from .models import Consulta

class ConsultaMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if request.user.is_authenticated and request.user.role == 'VETERINARIAN':
            consultas_pendientes = Consulta.objects.filter(
                veterinario=request.user,
                fecha=timezone.now().date(),
                estado='PENDIENTE'
            ).count()
            request.session['consultas_pendientes'] = consultas_pendientes

        return response 