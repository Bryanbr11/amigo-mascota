from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator

class User(AbstractUser):
    is_veterinario = models.BooleanField(default=False)
    is_secretaria = models.BooleanField(default=False)
    telefono = models.CharField(max_length=20, blank=True)
    direccion = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    especialidad = models.CharField(max_length=100, blank=True)
    biografia = models.TextField(blank=True)
    is_verified = models.BooleanField(default=False)
    license_number = models.CharField(max_length=50, blank=True)

    class Meta:
        db_table = 'users_user'
        verbose_name = 'usuario'
        verbose_name_plural = 'usuarios'

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip()

    def get_initials(self):
        return f"{self.first_name[0]}{self.last_name[0]}".upper() if self.first_name and self.last_name else self.username[:2].upper()

    def clean(self):
        if self.is_veterinario and not self.is_verified and not self._state.adding:
            raise ValidationError(_("Los veterinarios deben estar verificados antes del registro."))
        if self.is_secretaria and not self.is_staff:
            raise ValidationError(_("Las secretarias deben ser miembros del staff."))
        if self.is_veterinario and not self.license_number:
            raise ValidationError(_("Los veterinarios deben proporcionar un número de licencia."))

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def get_role_display(self):
        if self.is_superuser:
            return "Administrador"
        elif self.is_veterinario:
            return "Veterinario"
        elif self.is_secretaria:
            return "Secretaria"
        else:
            return "Cliente"

    @property
    def is_client(self):
        return not (self.is_veterinario or self.is_secretaria or self.is_superuser)

    def __str__(self):
        return f"{self.get_full_name()} - {self.get_role_display()}"