from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    license_number = forms.CharField(required=False, help_text='Requerido para veterinarios')
    
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'telefono', 'direccion', 'license_number')

    def clean(self):
        cleaned_data = super().clean()
        role = self.data.get('role')
        license_number = cleaned_data.get('license_number')
        
        if role == 'veterinario' and not license_number:
            raise ValidationError('Los veterinarios deben proporcionar un número de licencia')
        
        return cleaned_data

class CustomUserChangeForm(UserChangeForm):
    password = None

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Agregar clases de Tailwind a los campos
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'shadow-sm appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline focus:border-blue-500'
            })