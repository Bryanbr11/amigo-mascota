from rest_framework import serializers
from .models import Mascota, Especie

class EspecieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Especie
        fields = ['id', 'nombre', 'descripcion']

class MascotaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mascota
        fields = ['id', 'nombre', 'especie', 'raza', 'fecha_nacimiento', 'peso', 'foto', 'propietario', 'fecha_registro']
        read_only_fields = ['fecha_registro', 'propietario']

    def create(self, validated_data):
        validated_data['propietario'] = self.context['request'].user
        return super().create(validated_data)

class MascotaListSerializer(serializers.ModelSerializer):
    especie = serializers.StringRelatedField()

    class Meta:
        model = Mascota
        fields = ['id', 'nombre', 'especie', 'raza']

class MascotaDetailSerializer(MascotaSerializer):
    especie = EspecieSerializer(read_only=True)

    class Meta(MascotaSerializer.Meta):
        fields = MascotaSerializer.Meta.fields + ['fecha_nacimiento', 'peso', 'foto']