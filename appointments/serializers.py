from rest_framework import serializers
from .models import Appointment

class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ['id', 'mascota', 'veterinario', 'cliente', 'fecha', 'hora', 'estado', 'motivo', 'observaciones']
    def validate_fecha(self, value):
        today = timezone.now().date()
        max_date = today + timedelta(days=90)  # 3 meses desde hoy

        if value < today:
            raise serializers.ValidationError("No se pueden crear citas en fechas pasadas.")
        if value > max_date:
            raise serializers.ValidationError("No se pueden crear citas con más de 3 meses de anticipación.")

        return value

    def create(self, validated_data):
        user = self.context['request'].user
        if user.role not in ['CLIENT', 'ADMIN', 'SECRETARY']:
            raise serializers.ValidationError("No tienes permiso para crear citas.")
        return super().create(validated_data)