from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Consulta, HistorialConsulta
from mascotas.models import Mascota
from django.utils import timezone

User = get_user_model()

class ConsultaTestCase(TestCase):
    def setUp(self):
        self.veterinario = User.objects.create_user(username='vet', password='testpass123', role='VETERINARIO')
        self.cliente = User.objects.create_user(username='cliente', password='testpass123', role='CLIENTE')
        self.mascota = Mascota.objects.create(nombre='Firulais', propietario=self.cliente)
        self.consulta = Consulta.objects.create(
            mascota=self.mascota,
            veterinario=self.veterinario,
            fecha=timezone.now().date(),
            hora=timezone.now().time(),
            motivo='Revisión general'
        )

 def test_crear_consulta(self):
        self.client.login(username='vet', password='testpass123')
        response = self.client.post(reverse('consulta:crear_consulta'), {
            'mascota': self.mascota.id,
            'fecha': timezone.now().date(),
            'hora': timezone.now().time(),
            'motivo': 'Nueva consulta'
        })
        self.assertEqual(response.status_code, 302)  # Redirección después de crear
        self.assertEqual(Consulta.objects.count(), 2)  # Se ha creado una nueva consulta

    def test_editar_consulta(self):
        self.client.login(username='vet', password='testpass123')
        response = self.client.post(reverse('consulta:editar_consulta', args=[self.consulta.id]), {
            'mascota': self.mascota.id,
            'fecha': self.consulta.fecha,
            'hora': self.consulta.hora,
            'motivo': 'Motivo actualizado',
            'diagnostico': 'Nuevo diagnóstico',
            'tratamiento': 'Nuevo tratamiento'
        })
        self.assertEqual(response.status_code, 302)  # Redirección después de editar
        self.consulta.refresh_from_db()
        self.assertEqual(self.consulta.motivo, 'Motivo actualizado')
        self.assertEqual(HistorialConsulta.objects.count(), 1)  # Se ha creado un historial

    def test_finalizar_consulta(self):
        self.client.login(username='vet', password='testpass123')
        response = self.client.post(reverse('consulta:finalizar_consulta', args=[self.consulta.id]), {
            'diagnostico': 'Diagnóstico final',
            'tratamiento': 'Tratamiento prescrito',
            'notas_adicionales': 'Notas finales',
            'costo': 50.00
        })
        self.assertEqual(response.status_code, 302)  # Redirección después de finalizar
        self.consulta.refresh_from_db()
        self.assertEqual(self.consulta.estado, 'REALIZADA')
        self.assertEqual(self.consulta.costo, 50.00)

    def test_cancelar_consulta(self):
        self.client.login(username='cliente', password='testpass123')
        response = self.client.post(reverse('consulta:cancelar_consulta', args=[self.consulta.id]))
        self.assertEqual(response.status_code, 302)  # Redirección después de cancelar
        self.consulta.refresh_from_db()
        self.assertEqual(self.consulta.estado, 'CANCELADA')

    def test_lista_consultas_veterinario(self):
        self.client.login(username='vet', password='testpass123')
        response = self.client.get(reverse('consulta:lista_consultas'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Firulais')  # El nombre de la mascota debe aparecer en la lista

    def test_lista_consultas_cliente(self):
        self.client.login(username='cliente', password='testpass123')
        response = self.client.get(reverse('consulta:lista_consultas'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Firulais')  # El nombre de la mascota debe aparecer en la lista

    def test_detalle_consulta_veterinario(self):
        self.client.login(username='vet', password='testpass123')
        response = self.client.get(reverse('consulta:detalle_consulta', args=[self.consulta.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Revisión general')  # El motivo de la consulta debe aparecer en el detalle

    def test_detalle_consulta_cliente(self):
        self.client.login(username='cliente', password='testpass123')
        response = self.client.get(reverse('consulta:detalle_consulta', args=[self.consulta.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Revisión general')  # El motivo de la consulta debe aparecer en el detalle

    def test_acceso_no_autorizado(self):
        otro_cliente = User.objects.create_user(username='otro', password='testpass123', role='CLIENTE')
        self.client.login(username='otro', password='testpass123')
        response = self.client.get(reverse('consulta:detalle_consulta', args=[self.consulta.id]))
        self.assertEqual(response.status_code, 302)  # Redirección por falta de permisos