from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from finance.models import FinancialGoal, Organization
from datetime import date

User = get_user_model()

class FinancialGoalTests(TestCase):
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

    def test_create_goal(self):
        """Test creating a simple financial goal"""
        data = {
            'name': 'Save for Car',
            'target_amount': '25000.00',
            'current_amount': '5000.00',
            'deadline': str(date(2025, 12, 31)),
            'organization': self.organization.id
        }
        response = self.client.post('/api/v1/finance/goals/', data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['name'], 'Save for Car')
        self.assertEqual(response.data['target_amount'], '25000.00')
        self.assertEqual(float(response.data['progress_percentage']), 20.0)  # 5000/25000 * 100

    def test_goal_progress(self):
        """Test getting goal progress"""
        # Create a test goal first
        goal = FinancialGoal.objects.create(
            organization=self.organization,
            name='Emergency Fund',
            target_amount=10000.00,
            current_amount=2500.00,
            deadline=date(2025, 12, 31)
        )
        
        response = self.client.get(f'/api/v1/finance/goals/{goal.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], 'Emergency Fund')
        self.assertEqual(float(response.data['progress_percentage']), 25.0)
