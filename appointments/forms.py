from django import forms
from .models import Appointment
from django.contrib.auth import get_user_model
from mascotas.models import Mascota
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import datetime, time

User = get_user_model()

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['mascota', 'veterinario', 'cliente', 'fecha', 'hora', 'motivo', 'notas']
        widgets = {
            'fecha': forms.DateInput(attrs={
                'type': 'date',
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm',
                'required': 'required'
            }),
            'hora': forms.TimeInput(attrs={
                'type': 'time',
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm',
                'required': 'required'
            }),
            'motivo': forms.Textarea(attrs={
                'rows': 3,
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm',
                'required': 'required',
                'placeholder': 'Describe el motivo de la consulta'
            }),
            'notas': forms.Textarea(attrs={
                'rows': 3,
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm',
                'placeholder': 'Notas adicionales (opcional)'
            }),
            'mascota': forms.Select(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm',
                'required': 'required'
            }),
            'veterinario': forms.Select(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm',
                'required': 'required'
            }),
            'cliente': forms.Select(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm',
                'required': 'required'
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrar solo veterinarios activos
        self.fields['veterinario'].queryset = User.objects.filter(
            is_veterinario=True,
            is_active=True
        )
        # Filtrar solo clientes activos
        self.fields['cliente'].queryset = User.objects.filter(
            is_active=True
        ).exclude(
            is_veterinario=True
        ).exclude(
            is_superuser=True
        ).exclude(
            is_secretaria=True
        )

        # Marcar campos requeridos
        for field_name in ['mascota', 'veterinario', 'cliente', 'fecha', 'hora', 'motivo']:
            self.fields[field_name].required = True

    def clean(self):
        cleaned_data = super().clean()
        fecha = cleaned_data.get('fecha')
        hora = cleaned_data.get('hora')
        
        if fecha and hora:
            # Verificar que la fecha no sea en el pasado
            fecha_hora = timezone.make_aware(datetime.combine(fecha, hora))
            now = timezone.now()
            
            if fecha_hora < now:
                raise ValidationError({
                    'fecha': "La fecha y hora de la cita no pueden ser en el pasado.",
                    'hora': "La fecha y hora de la cita no pueden ser en el pasado."
                })
            
            # Verificar horario de atención (8:00 AM a 6:00 PM)
            hora_inicio = time(8, 0)  # 8:00 AM
            hora_fin = time(18, 0)    # 6:00 PM
            
            if hora < hora_inicio or hora >= hora_fin:
                raise ValidationError({
                    'hora': "Las citas solo pueden programarse entre las 8:00 AM y las 6:00 PM."
                })
            
            # Verificar si ya existe una cita para ese veterinario en esa fecha y hora
            citas_existentes = Appointment.objects.filter(
                veterinario=cleaned_data.get('veterinario'),
                fecha=fecha,
                hora=hora
            )
            if self.instance.pk:
                citas_existentes = citas_existentes.exclude(pk=self.instance.pk)
            
            if citas_existentes.exists():
                raise ValidationError({
                    'hora': "Ya existe una cita programada para este veterinario en esta fecha y hora."
                })
        
        return cleaned_data

class AppointmentUpdateForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['fecha', 'hora', 'motivo', 'notas', 'veterinario']
        widgets = {
            'fecha': forms.DateInput(attrs={
                'type': 'date',
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm',
                'required': 'required'
            }),
            'hora': forms.TimeInput(attrs={
                'type': 'time',
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm',
                'required': 'required'
            }),
            'motivo': forms.Textarea(attrs={
                'rows': 3,
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm',
                'required': 'required'
            }),
            'notas': forms.Textarea(attrs={
                'rows': 3,
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm'
            }),
            'veterinario': forms.Select(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm',
                'required': 'required'
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['veterinario'].queryset = User.objects.filter(
            is_veterinario=True,
            is_active=True
        )
        
        # Marcar campos requeridos
        for field_name in ['fecha', 'hora', 'motivo', 'veterinario']:
            self.fields[field_name].required = True

    def clean(self):
        cleaned_data = super().clean()
        fecha = cleaned_data.get('fecha')
        hora = cleaned_data.get('hora')
        
        if fecha and hora:
            # Verificar que la fecha no sea en el pasado
            fecha_hora = timezone.make_aware(datetime.combine(fecha, hora))
            now = timezone.now()
            
            if fecha_hora < now:
                raise ValidationError({
                    'fecha': "La fecha y hora de la cita no pueden ser en el pasado.",
                    'hora': "La fecha y hora de la cita no pueden ser en el pasado."
                })
            
            # Verificar horario de atención (8:00 AM a 6:00 PM)
            hora_inicio = time(8, 0)  # 8:00 AM
            hora_fin = time(18, 0)    # 6:00 PM
            
            if hora < hora_inicio or hora >= hora_fin:
                raise ValidationError({
                    'hora': "Las citas solo pueden programarse entre las 8:00 AM y las 6:00 PM."
                })
            
            # Verificar si ya existe una cita para ese veterinario en esa fecha y hora
            citas_existentes = Appointment.objects.filter(
                veterinario=cleaned_data.get('veterinario'),
                fecha=fecha,
                hora=hora
            ).exclude(pk=self.instance.pk)
            
            if citas_existentes.exists():
                raise ValidationError({
                    'hora': "Ya existe una cita programada para este veterinario en esta fecha y hora."
                })
        
        return cleaned_data

class AppointmentStatusForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['estado', 'notas']
        widgets = {
            'estado': forms.Select(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm',
                'required': 'required'
            }),
            'notas': forms.Textarea(attrs={
                'rows': 3,
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm'
            })
        }