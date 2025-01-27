from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from .models import Appointment, Notification
from mascotas.models import Mascota
from datetime import datetime, timedelta
from django.utils import timezone
from .tasks import enviar_recordatorios_citas
from django.contrib.auth import get_user_model

User = get_user_model()

class AppointmentTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin = User.objects.create_user(username='admin', password='admin123', role='ADMIN')
        self.veterinario = User.objects.create_user(username='vet', password='vet123', role='VETERINARIO')
        self.cliente = User.objects.create_user(username='cliente', password='cliente123', role='CLIENTE')
        self.mascota = Mascota.objects.create(nombre='Firulais', propietario=self.cliente)
        self.appointment = Appointment.objects.create(
            mascota=self.mascota,
            veterinario=self.veterinario,
            cliente=self.cliente,
            fecha=timezone.now().date() + timedelta(days=1),
            hora=datetime.now().time(),
            motivo='Revisión'
        )

    def test_list_appointments(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.get(reverse('appointment-list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_create_appointment(self):
        self.client.force_authenticate(user=self.cliente)
        data = {
            'mascota': self.mascota.id,
            'veterinario': self.veterinario.id,
            'fecha': (timezone.now() + timedelta(days=2)).date(),
            'hora': datetime.now().time(),
            'motivo': 'Nueva revisión'
        }
        response = self.client.post(reverse('appointment-list'), data)
        self.assertEqual(response.status_code, 201)

    def test_update_appointment(self):
        self.client.force_authenticate(user=self.cliente)
        data = {'motivo': 'Motivo actualizado'}
        response = self.client.patch(reverse('appointment-detail', args=[self.appointment.id]), data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Appointment.objects.get(id=self.appointment.id).motivo, 'Motivo actualizado')

    def test_delete_appointment(self):
        self.client.force_authenticate(user=self.cliente)
        response = self.client.delete(reverse('appointment-detail', args=[self.appointment.id]))
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Appointment.objects.count(), 0)

    def test_cant_modify_appointment_less_than_2_hours(self):
        self.client.force_authenticate(user=self.cliente)
        self.appointment.fecha = timezone.now().date()
        self.appointment.hora = (timezone.now() + timedelta(hours=1)).time()
        self.appointment.save()
        data = {'motivo': 'Intento de modificación'}
        response = self.client.patch(reverse('appointment-detail', args=[self.appointment.id]), data)
        self.assertEqual(response.status_code, 400)

        # appointments/tests.py


User = get_user_model()

class RecordatoriosCitasTest(TestCase):
    def setUp(self):
        self.cliente = User.objects.create_user(username='cliente', email='cliente@example.com')
        self.veterinario = User.objects.create_user(username='vet', email='vet@example.com')
        self.cita_manana = Appointment.objects.create(
            cliente=self.cliente,
            veterinario=self.veterinario,
            fecha=timezone.now().date() + timezone.timedelta(days=1),
            hora=timezone.now().time(),
            estado='PENDIENTE'
        )

    def test_enviar_recordatorios_citas(self):
        result = enviar_recordatorios_citas()
        self.assertIn('Enviados 1 recordatorios', result)
        self.assertEqual(Notification.objects.count(), 1)
        self.assertEqual(Notification.objects.first().user, self.cliente)