from rest_framework.permissions import BasePermission

class IsVeterinarian(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'VETERINARIAN'

class IsSecretary(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'SECRETARY'

class IsClient(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'CLIENT'

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'ADMIN'