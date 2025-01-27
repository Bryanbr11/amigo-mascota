from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from ..models import Consulta, HistorialConsulta
from ..serializers import ConsultaSerializer, HistorialConsultaSerializer
from ..permissions import IsVeterinarioMixin, IsOwnerOrVeterinarioMixin

class ConsultaViewSet(IsOwnerOrVeterinarioMixin, viewsets.ModelViewSet):
    queryset = Consulta.objects.all()
    serializer_class = ConsultaSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.role == 'VETERINARIO':
            return Consulta.objects.filter(veterinario=self.request.user)
        return Consulta.objects.filter(mascota__propietario=self.request.user)

class HistorialConsultaViewSet(IsVeterinarioMixin, viewsets.ReadOnlyModelViewSet):
    queryset = HistorialConsulta.objects.all()
    serializer_class = HistorialConsultaSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return HistorialConsulta.objects.filter(consulta__veterinario=self.request.user)