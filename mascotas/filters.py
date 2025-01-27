import django_filters
from .models import Mascota

class MascotaFilter(django_filters.FilterSet):
    nombre = django_filters.CharFilter(lookup_expr='icontains')
    especie = django_filters.CharFilter(lookup_expr='icontains')
    raza = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Mascota
        fields = ['nombre', 'especie', 'raza']