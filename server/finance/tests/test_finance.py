from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from ..models import Income, Expense
from django.contrib.auth import get_user_model

User = get_user_model()

class FinanceTests(TestCase):
    """Test cases for the finance app"""
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.client.login(username='testuser', password='testpass123')

    def test_create_income(self):
        url = reverse('income-list')  # Correct URL name
        data = {
            'amount': 1000.00,
            'description': 'Salary for January',
            'income_type': 'SALARY'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Income.objects.count(), 1)
        self.assertEqual(Income.objects.get().description, 'Salary for January')

    def test_create_expense(self):
        url = reverse('expense-list')  # Correct URL name
        data = {
            'amount': 500.00,
            'description': 'Grocery Shopping',
            'category': 'FOOD'  # Assuming you have a category field
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Expense.objects.count(), 1)
        self.assertEqual(Expense.objects.get().description, 'Grocery Shopping')

    def test_retrieve_income(self):
        Income.objects.create(user=self.user, amount=1000.00, description='Salary', income_type='SALARY')
        url = reverse('income-list')  # Correct URL name
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_expense(self):
        Expense.objects.create(user=self.user, amount=200.00, description='Utilities', category='BILLS')
        url = reverse('expense-list')  # Correct URL name
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
