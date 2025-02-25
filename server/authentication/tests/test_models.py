from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from authentication.models import Organization, Role, User

class OrganizationModelTest(TestCase):
    def test_organization_creation(self):
        org = Organization.objects.create(
            name="Test Organization",
            code="TEST123",
            address="123 Test Street"
        )
        self.assertEqual(org.name, "Test Organization")
        self.assertEqual(org.code, "TEST123")
        
    def test_auto_code_generation(self):
        org = Organization.objects.create(
            name="Test Organization 2",
            address="123 Test Street"
        )
        self.assertIsNotNone(org.code)
        self.assertEqual(len(org.code), 8)

    def test_unique_name_constraint(self):
        org1 = Organization.objects.create(name="Test Org")
        with self.assertRaises(Exception):
            Organization.objects.create(name="Test Org")

class RoleModelTest(TestCase):
    def setUp(self):
        self.role = Role.objects.create(name='Admin')
    
    def test_role_creation(self):
        self.assertEqual(self.role.name, 'Admin')
        self.assertEqual(str(self.role), 'Administrator')

    def test_invalid_role_choice(self):
        with self.assertRaises(ValidationError):
            role = Role(name='InvalidRole')
            role.clean()

class UserModelTest(TestCase):
    def setUp(self):
        self.org = Organization.objects.create(
            name="Test Organization",
            code="TEST123"
        )
        self.role = Role.objects.create(name='Admin')
        
    def test_create_user_minimal(self):
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'test@example.com')
        self.assertTrue(user.check_password('testpass123'))
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_user_full(self):
        user = User.objects.create_user(
            username='testuser2',
            email='test2@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )
        user.organization = self.org
        user.role = self.role
        user.save()

        self.assertEqual(user.username, 'testuser2')
        self.assertEqual(user.email, 'test2@example.com')
        self.assertEqual(user.first_name, 'Test')
        self.assertEqual(user.last_name, 'User')
        self.assertEqual(user.organization, self.org)
        self.assertEqual(user.role, self.role)
        self.assertTrue(user.check_password('testpass123'))
