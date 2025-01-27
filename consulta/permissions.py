from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied

class IsVeterinarioMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.role == 'VETERINARIO'

    def handle_no_permission(self):
        raise PermissionDenied("Solo los veterinarios pueden acceder a esta página.")

class IsOwnerOrVeterinarioMixin(UserPassesTestMixin):
    def test_func(self):
        consulta = self.get_object()
        return (self.request.user.is_authenticated and 
                (self.request.user.role == 'VETERINARIO' or 
                 consulta.mascota.propietario == self.request.user))

    def handle_no_permission(self):
        raise PermissionDenied("No tienes permiso para acceder a esta consulta.")