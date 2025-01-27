from django import forms
from .models import Mascota
from datetime import date

class MascotaForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.especie:
            self.fields['raza'].choices = self.instance.RAZAS_POR_ESPECIE.get(
                self.instance.especie, [('OTRO', 'Otro')]
            )
        self.fields['fecha_nacimiento'].widget.attrs['max'] = date.today().isoformat()

    class Meta:
        model = Mascota
        fields = ['nombre', 'especie', 'raza', 'fecha_nacimiento', 'peso', 'foto']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm',
                'placeholder': 'Nombre de la mascota'
            }),
            'especie': forms.Select(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm',
                'onchange': 'updateRazas(this.value)'
            }),
            'raza': forms.Select(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm'
            }),
            'fecha_nacimiento': forms.DateInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm',
                'type': 'date',
                'max': date.today().isoformat()
            }),
            'peso': forms.NumberInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm',
                'step': '0.1',
                'min': '0'
            }),
            'foto': forms.FileInput(attrs={
                'class': 'mt-1 block w-full text-sm text-gray-900 border border-gray-300 rounded-lg cursor-pointer bg-gray-50 focus:outline-none'
            })
        }

    def clean_fecha_nacimiento(self):
        fecha_nacimiento = self.cleaned_data['fecha_nacimiento']
        if fecha_nacimiento > date.today():
            raise forms.ValidationError("La fecha de nacimiento no puede ser en el futuro.")
        return fecha_nacimiento

    def clean_peso(self):
        peso = self.cleaned_data['peso']
        if peso <= 0:
            raise forms.ValidationError("El peso debe ser mayor que cero.")
        return peso
