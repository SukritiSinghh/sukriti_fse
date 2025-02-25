from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from finance.models import Income, Expense
from decimal import Decimal

User = get_user_model()

class FinanceEndpointTests(TestCase):
    def setUp(self):
        # Create test user and authenticate
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )
        self.client.force_authenticate(user=self.user)

    def test_create_income(self):
        """Test creating a simple income record"""
        data = {
            'amount': '1000.00',
            'description': 'Test Income',
            'income_type': 'SALARY'
        }
        response = self.client.post('/api/v1/finance/income/', data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['amount'], '1000.00')
        self.assertEqual(response.data['description'], 'Test Income')

    def test_create_expense(self):
        """Test creating a simple expense record"""
        data = {
            'amount': '500.00',
            'description': 'Test Expense',
            'category': 'FOOD'
        }
        response = self.client.post('/api/v1/finance/expenses/', data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['amount'], '500.00')
        self.assertEqual(response.data['description'], 'Test Expense')
