from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import User

class UserModelTest(TestCase):
    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(username='testuser', email='test@example.com', password='testpass123', role='client')
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'test@example.com')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertEqual(user.role, 'client')

    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser(username='admin', email='admin@example.com', password='adminpass123')
        self.assertEqual(admin_user.username, 'admin')
        self.assertEqual(admin_user.email, 'admin@example.com')
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        self.assertEqual(admin_user.role, 'admin')

class UserRegistrationTest(TestCase):
    def test_user_registration(self):
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'testpass123',
            'password2': 'testpass123',
            'role': 'client'
        })
        self.assertEqual(response.status_code, 302)  # Redirección después del registro exitoso
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_vet_registration(self):
        response = self.client.post(reverse('vet_register'), {
            'username': 'newvet',
            'email': 'newvet@example.com',
            'password1': 'testpass123',
            'password2': 'testpass123',
            'license_number': 'VET12345'
        })
        self.assertEqual(response.status_code, 302)  # Redirección después del registro
        new_vet = User.objects.get(username='newvet')
        self.assertEqual(new_vet.role, 'vet')
        self.assertFalse(new_vet.is_verified)

class UserLoginTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpass123', role='client')

    def test_user_login(self):
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'testpass123'
        })
        self.assertEqual(response.status_code, 302)  # Redirección después del login exitoso

    def test_user_logout(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)  # Redirección después del logout

class RoleAccessTest(TestCase):
    def setUp(self):
        self.client_user = User.objects.create_user(username='client', email='client@example.com', password='testpass123', role='client')
        self.vet_user = User.objects.create_user(username='vet', email='vet@example.com', password='testpass123', role='vet', is_verified=True)
        self.secretary_user = User.objects.create_user(username='secretary', email='secretary@example.com', password='testpass123', role='secretary', is_staff=True)
        self.admin_user = User.objects.create_superuser(username='admin', email='admin@example.com', password='adminpass123')

    def test_client_access(self):
        self.client.login(username='client', password='testpass123')
        response = self.client.get(reverse('client_dashboard'))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('vet_dashboard'))
        self.assertEqual(response.status_code, 302)  # Redirección por falta de permisos

    def test_vet_access(self):
        self.client.login(username='vet', password='testpass123')
        response = self.client.get(reverse('vet_dashboard'))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('admin_dashboard'))
        self.assertEqual(response.status_code, 302)  # Redirección por falta de permisos

    def test_secretary_access(self):
        self.client.login(username='secretary', password='testpass123')
        response = self.client.get(reverse('secretary_dashboard'))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('vet_dashboard'))
        self.assertEqual(response.status_code, 302)  # Redirección por falta de permisos

    def test_admin_access(self):
        self.client.login(username='admin', password='adminpass123')
        response = self.client.get(reverse('admin_dashboard'))
        self.assertEqual(response.status_code, 200)