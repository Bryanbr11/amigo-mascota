from django import forms
from .models import FichaMedica
from mascotas.models import Mascota

class FichaMedicaForm(forms.ModelForm):
    mascota = forms.ModelChoiceField(
        queryset=Mascota.objects.all(), 
        label='Mascota',
        help_text='Selecciona la mascota para esta ficha médica'
    )

    class Meta:
        model = FichaMedica
        fields = [
            'mascota', 
            'peso', 
            'temperatura', 
            'diagnostico_previo', 
            'tratamientos_anteriores', 
            'motivo_consulta', 
            'sintomas', 
            'diagnostico_actual', 
            'tratamiento_recomendado', 
            'estado', 
            'proxima_consulta', 
            'medicamentos'
        ]
        widgets = {
            'motivo_consulta': forms.Textarea(attrs={'rows': 3}),
            'sintomas': forms.Textarea(attrs={'rows': 3}),
            'diagnostico_actual': forms.Textarea(attrs={'rows': 3}),
            'tratamiento_recomendado': forms.Textarea(attrs={'rows': 3}),
            'diagnostico_previo': forms.Textarea(attrs={'rows': 3}),
            'tratamientos_anteriores': forms.Textarea(attrs={'rows': 3}),
            'medicamentos': forms.Textarea(attrs={'rows': 3}),
        }