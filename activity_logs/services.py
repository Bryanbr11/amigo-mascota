from .models import ActivityLog

def log_activity(user, action_type, details, request=None, content_type=None, object_id=None):
    """
    Registra una actividad en el sistema.
    
    Args:
        user: Usuario que realiza la acción
        action_type: Tipo de acción (CREATE, UPDATE, DELETE, LOGIN, LOGOUT)
        details: Descripción de la acción
        request: Objeto request para obtener la IP (opcional)
        content_type: Tipo de contenido afectado (opcional)
        object_id: ID del objeto afectado (opcional)
    """
    ip_address = None
    if request and hasattr(request, 'activity_log'):
        ip_address = request.activity_log.get('ip_address')

    ActivityLog.objects.create(
        user=user,
        action_type=action_type,
        details=details,
        ip_address=ip_address,
        content_type=content_type or '',
        object_id=object_id or ''
    ) 