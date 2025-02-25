from django.test import TestCase
from django.contrib.auth import get_user_model
from finance.models import Income, Expense, FinancialGoal
from decimal import Decimal

User = get_user_model()

class FinanceModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )

    def test_create_income(self):
        """Test creating an income record"""
        income = Income.objects.create(
            user=self.user,
            amount=1000.00,
            description='Test Income',
            income_type='SALARY'
        )
        self.assertEqual(income.amount, Decimal('1000.00'))
        self.assertEqual(income.description, 'Test Income')
        self.assertEqual(income.income_type, 'SALARY')
        self.assertEqual(income.user, self.user)

    def test_create_expense(self):
        """Test creating an expense record"""
        expense = Expense.objects.create(
            user=self.user,
            amount=500.00,
            description='Test Expense',
            category='FOOD'
        )
        self.assertEqual(expense.amount, Decimal('500.00'))
        self.assertEqual(expense.description, 'Test Expense')
        self.assertEqual(expense.category, 'FOOD')
        self.assertEqual(expense.user, self.user)

    def test_financial_goal(self):
        """Test creating a financial goal"""
        goal = FinancialGoal.objects.create(
            name='Test Goal',
            target_amount=5000.00,
            current_amount=1000.00,
            deadline='2025-12-31'
        )
        self.assertEqual(goal.name, 'Test Goal')
        self.assertEqual(goal.target_amount, Decimal('5000.00'))
        self.assertEqual(goal.current_amount, Decimal('1000.00'))
        # Test progress calculation
        self.assertEqual(goal.progress_percentage(), 20)  # (1000/5000) * 100
