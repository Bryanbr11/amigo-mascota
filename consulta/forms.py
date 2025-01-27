from django import forms
from .models import Consulta

class ConsultaForm(forms.ModelForm):
    class Meta:
        model = Consulta
        fields = ['mascota', 'motivo', 'sintomas', 'signos_clinicos', 'peso', 'diagnostico', 'tratamiento', 'notas_adicionales', 'costo', 'tipo_servicio']
        widgets = {
            'motivo': forms.Textarea(attrs={'class': 'shadow-sm focus:ring-blue-500 focus:border-blue-500 block w-full sm:text-sm border-gray-300 rounded-md', 'rows': 3}),
            'sintomas': forms.Textarea(attrs={'class': 'shadow-sm focus:ring-blue-500 focus:border-blue-500 block w-full sm:text-sm border-gray-300 rounded-md', 'rows': 4}),
            'signos_clinicos': forms.Textarea(attrs={'class': 'shadow-sm focus:ring-blue-500 focus:border-blue-500 block w-full sm:text-sm border-gray-300 rounded-md', 'rows': 4}),
            'diagnostico': forms.Textarea(attrs={'class': 'shadow-sm focus:ring-blue-500 focus:border-blue-500 block w-full sm:text-sm border-gray-300 rounded-md', 'rows': 4}),
            'tratamiento': forms.Textarea(attrs={'class': 'shadow-sm focus:ring-blue-500 focus:border-blue-500 block w-full sm:text-sm border-gray-300 rounded-md', 'rows': 4}),
            'notas_adicionales': forms.Textarea(attrs={'class': 'shadow-sm focus:ring-blue-500 focus:border-blue-500 block w-full sm:text-sm border-gray-300 rounded-md', 'rows': 4}),
            'mascota': forms.Select(attrs={'class': 'mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm rounded-md'}),
            'tipo_servicio': forms.Select(attrs={'class': 'mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm rounded-md'}),
            'peso': forms.NumberInput(attrs={'class': 'shadow-sm focus:ring-blue-500 focus:border-blue-500 block w-full sm:text-sm border-gray-300 rounded-md', 'step': '0.01'}),
            'costo': forms.NumberInput(attrs={'class': 'shadow-sm focus:ring-blue-500 focus:border-blue-500 block w-full sm:text-sm border-gray-300 rounded-md', 'step': '0.01'}),
        }

class FinalizarConsultaForm(forms.ModelForm):
    class Meta:
        model = Consulta
        fields = ['diagnostico', 'tratamiento', 'notas_adicionales', 'costo', 'estado']
        widgets = {
            'diagnostico': forms.Textarea(attrs={'class': 'shadow-sm focus:ring-blue-500 focus:border-blue-500 block w-full sm:text-sm border-gray-300 rounded-md', 'rows': 4}),
            'tratamiento': forms.Textarea(attrs={'class': 'shadow-sm focus:ring-blue-500 focus:border-blue-500 block w-full sm:text-sm border-gray-300 rounded-md', 'rows': 4}),
            'notas_adicionales': forms.Textarea(attrs={'class': 'shadow-sm focus:ring-blue-500 focus:border-blue-500 block w-full sm:text-sm border-gray-300 rounded-md', 'rows': 4}),
            'costo': forms.NumberInput(attrs={'class': 'shadow-sm focus:ring-blue-500 focus:border-blue-500 block w-full sm:text-sm border-gray-300 rounded-md', 'step': '0.01'}),
            'estado': forms.Select(attrs={'class': 'mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm rounded-md'}),
        }