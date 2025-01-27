from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from dashboard.models import Mascota, Cita, Especie
from datetime import date

User = get_user_model()

class Command(BaseCommand):
    help = 'Crea datos iniciales para la aplicación'

    def handle(self, *args, **kwargs):
        # Crear especies básicas
        perro = Especie.objects.create(
            nombre='Perro',
            descripcion='Canis lupus familiaris'
        )
        gato = Especie.objects.create(
            nombre='Gato',
            descripcion='Felis catus'
        )
        ave = Especie.objects.create(
            nombre='Ave',
            descripcion='Aves domésticas'
        )

        # Crear superusuario
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@example.com',
                password='admin123456',
                first_name='Admin',
                last_name='Usuario'
            )

        # Crear veterinario
        veterinario = User.objects.create_user(
            username='veterinario',
            password='vet123456',
            is_veterinario=True,
            first_name='Juan',
            last_name='Pérez',
            email='veterinario@example.com',
            telefono='123456789',
            direccion='Calle Principal 123',
            especialidad='Medicina General'
        )

        # Crear secretaria
        secretaria = User.objects.create_user(
            username='secretaria',
            password='sec123456',
            is_secretaria=True,
            first_name='María',
            last_name='García',
            email='secretaria@example.com',
            telefono='987654321',
            direccion='Avenida Central 456'
        )

        # Crear cliente
        cliente = User.objects.create_user(
            username='cliente',
            password='cli123456',
            first_name='Pedro',
            last_name='López',
            email='cliente@example.com',
            telefono='555555555',
            direccion='Plaza Mayor 789'
        )

        self.stdout.write(self.style.SUCCESS('Datos iniciales creados exitosamente')) 