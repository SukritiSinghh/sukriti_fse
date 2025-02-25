from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from authentication.models import Organization, Role, User
from django.core.exceptions import ValidationError

class AuthenticationViewsTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.org = Organization.objects.create(
            name="Test Organization",
            code="TEST123"
        )
        self.role = Role.objects.create(name='Admin')
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpass123',
            'confirm_password': 'testpass123',
            'organization': self.org.id,
            'role': self.role.id
        }
        self.login_data = {
            'username': 'testuser',
            'password': 'testpass123'
        }

    def test_user_registration_minimal(self):
        """Test user registration with minimal required fields"""
        url = reverse('user-register')
        response = self.client.post(url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username='testuser').exists())
        user = User.objects.get(username='testuser')
        self.assertEqual(user.organization.id, self.org.id)
        self.assertEqual(user.role.id, self.role.id)
        self.assertIn('user', response.data)
        self.assertIn('message', response.data)

    def test_user_registration_with_names(self):
        """Test user registration with optional name fields"""
        self.user_data.update({
            'first_name': 'Test',
            'last_name': 'User'
        })
        url = reverse('user-register')
        response = self.client.post(url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = User.objects.get(username='testuser')
        self.assertEqual(user.first_name, 'Test')
        self.assertEqual(user.last_name, 'User')

    def test_user_registration_invalid_data(self):
        """Test user registration with invalid data"""
        invalid_data = self.user_data.copy()
        invalid_data['password'] = 'pass1'
        invalid_data['confirm_password'] = 'pass2'
        url = reverse('user-register')
        response = self.client.post(url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data)

    def test_user_login_success(self):
        """Test successful user login"""
        # Create user first
        url = reverse('user-register')
        response = self.client.post(url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Now try to login
        url = reverse('token_obtain_pair')
        response = self.client.post(url, self.login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_user_login_invalid_credentials(self):
        """Test login with invalid credentials"""
        url = reverse('token_obtain_pair')
        invalid_data = {
            'username': 'testuser',
            'password': 'wrongpassword'
        }
        response = self.client.post(url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_registration_duplicate_username(self):
        """Test registration with duplicate username"""
        # Create first user
        url = reverse('user-register')
        response = self.client.post(url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Try to create second user with same username
        duplicate_data = self.user_data.copy()
        duplicate_data['email'] = 'another@example.com'
        response = self.client.post(url, duplicate_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('username', response.data)
