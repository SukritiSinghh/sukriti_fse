import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from rest_framework import status
from finance.models import Income, Expense, FinancialReport
from authentication.models import Organization  # Updated import
from decimal import Decimal
import os
import tempfile
from datetime import date, timedelta

User = get_user_model()

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def test_organization():
    return Organization.objects.create(
        name='Test Organization',
        code='TEST123',
        address='123 Test St'
    )

@pytest.fixture
def test_user(test_organization):
    user = User.objects.create_user(
        username='testuser',
        email='testuser@example.com',
        password='testpass123'
    )
    user.organization = test_organization
    user.save()
    return user

@pytest.fixture
def test_file():
    with tempfile.NamedTemporaryFile(suffix='.csv', delete=False) as tmp:
        tmp.write(b'test,data\n1,2\n')
    return tmp.name

@pytest.fixture
def test_income(test_user):
    return Income.objects.create(
        user=test_user,
        amount=1000.00,
        description='Test Income',
        income_type='SALARY'
    )

@pytest.fixture
def test_expense(test_user):
    return Expense.objects.create(
        user=test_user,
        amount=500.00,
        description='Test Expense',
        category='FOOD'
    )

@pytest.mark.django_db
class TestFinance:
    def test_create_income(self, api_client, test_user):
        api_client.force_authenticate(user=test_user)
        url = '/api/v1/finance/income/'
        data = {
            'amount': '2000.00',
            'description': 'Monthly Salary',
            'income_type': 'SALARY'
        }
        response = api_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['amount'] == '2000.00'
        assert response.data['income_type'] == 'SALARY'

    def test_create_expense(self, api_client, test_user):
        api_client.force_authenticate(user=test_user)
        url = '/api/v1/finance/expenses/'
        data = {
            'amount': '150.00',
            'description': 'Groceries',
            'category': 'FOOD'
        }
        response = api_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['amount'] == '150.00'
        assert response.data['category'] == 'FOOD'

    def test_get_income_summary(self, api_client, test_user, test_income):
        api_client.force_authenticate(user=test_user)
        url = '/api/v1/finance/income/summary/'
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert 'this_month' in response.data
        assert 'this_year' in response.data
        assert 'today' in response.data

    def test_get_expense_summary(self, api_client, test_user, test_expense):
        api_client.force_authenticate(user=test_user)
        url = '/api/v1/finance/expenses/summary/'
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert 'this_month' in response.data
        assert 'this_year' in response.data
        assert 'today' in response.data

    def test_upload_document(self, api_client, test_user, test_file):
        api_client.force_authenticate(user=test_user)
        url = '/api/v1/finance/reports/'  
        with open(test_file, 'rb') as fp:
            data = {
                'title': 'Test Report',
                'file': fp,
                'report_type': 'INCOME',
                'year': 2025
            }
            response = api_client.post(url, data, format='multipart')
        assert response.status_code == status.HTTP_201_CREATED
        assert 'id' in response.data

    def test_list_documents(self, api_client, test_user):
        api_client.force_authenticate(user=test_user)
        url = '/api/v1/finance/reports/'
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def teardown_method(self, method):
        # Clean up any test files
        for filename in os.listdir('.'):
            if filename.endswith('.csv'):
                try:
                    os.remove(filename)
                except OSError:
                    pass
