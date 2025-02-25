from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework.test import APIClient
from finance.models import Income, Expense, Organization

User = get_user_model()

class FinancialSummaryTests(TestCase):
    def setUp(self):
        # Create test user and authenticate
        self.client = APIClient()
        
        # Create test organization
        self.organization = Organization.objects.create(
            name='Test Org',
            code='TEST001'
        )
        
        # Create user and then set organization
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )
        self.user.organization = self.organization
        self.user.save()
        
        self.client.force_authenticate(user=self.user)

        # Create some test data
        today = timezone.localtime().date()
        today_datetime = timezone.make_aware(timezone.datetime.combine(today, timezone.datetime.min.time()))
        
        Income.objects.create(
            user=self.user,
            amount=1000.00,
            description='January Salary',
            income_type='SALARY',
            date=today_datetime
        )
        
        Expense.objects.create(
            user=self.user,
            amount=500.00,
            description='January Rent',
            category='HOUSING',
            date=today_datetime
        )

    def test_income_summary(self):
        """Test getting income summary"""
        response = self.client.get('/api/v1/finance/income/summary/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('this_month' in response.data)
        self.assertTrue('this_year' in response.data)
        self.assertEqual(float(response.data['today']), 1000.00)
        self.assertEqual(float(response.data['this_month']), 1000.00)
        self.assertEqual(float(response.data['this_year']), 1000.00)

    def test_expense_summary(self):
        """Test getting expense summary"""
        response = self.client.get('/api/v1/finance/expenses/summary/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('this_month' in response.data)
        self.assertTrue('this_year' in response.data)
        self.assertEqual(float(response.data['today']), 500.00)
        self.assertEqual(float(response.data['this_month']), 500.00)
        self.assertEqual(float(response.data['this_year']), 500.00)
