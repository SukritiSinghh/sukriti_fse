from django.test import TestCase
from django.contrib.auth import get_user_model
from finance.models import Income, Expense
from finance.serializers import IncomeSerializer, ExpenseSerializer
from decimal import Decimal

User = get_user_model()

class FinanceSerializerTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )
        
        # Create test data
        self.income_data = {
            'amount': '1000.00',
            'description': 'Test Income',
            'income_type': 'SALARY',
            'user': self.user.id
        }
        
        self.expense_data = {
            'amount': '500.00',
            'description': 'Test Expense',
            'category': 'FOOD',
            'user': self.user.id
        }

    def test_income_serializer_valid(self):
        """Test income serializer with valid data"""
        serializer = IncomeSerializer(data=self.income_data)
        self.assertTrue(serializer.is_valid())

    def test_expense_serializer_valid(self):
        """Test expense serializer with valid data"""
        serializer = ExpenseSerializer(data=self.expense_data)
        self.assertTrue(serializer.is_valid())

    def test_income_serializer_invalid(self):
        """Test income serializer with invalid data"""
        invalid_data = self.income_data.copy()
        invalid_data['amount'] = 'not a number'
        serializer = IncomeSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())

    def test_expense_serializer_invalid(self):
        """Test expense serializer with invalid data"""
        invalid_data = self.expense_data.copy()
        invalid_data['amount'] = 'not a number'
        serializer = ExpenseSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
