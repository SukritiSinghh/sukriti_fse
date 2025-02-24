import requests
import os
from django.core.wsgi import get_wsgi_application
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'insuretech.settings')
application = get_wsgi_application()

from authentication.models import Organization
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

def setup_test_data():
    # Create test organization if it doesn't exist
    org, _ = Organization.objects.get_or_create(
        name='Test Organization',
        defaults={
            'code': 'TEST123',
            'address': '123 Test St'
        }
    )

    # Create test user if it doesn't exist
    user, created = User.objects.get_or_create(
        username='testuser',
        defaults={
            'email': 'testuser@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'is_active': True,
            'password': make_password('testpass123'),
            'organization': org  # Set organization during creation
        }
    )
    
    # If user already existed, make sure password and organization are set
    if not created:
        user.set_password('testpass123')
        user.organization = org
        user.save()

    # Get JWT token for authentication
    refresh = RefreshToken.for_user(user)
    return str(refresh.access_token)

def test_upload_and_process():
    base_url = "http://localhost:8000"
    token = setup_test_data()
    headers = {
        'Authorization': f'Bearer {token}'
    }

    # Test Balance Sheet Upload
    with open('test_data/balance_sheet_2024.csv', 'rb') as f:
        files = {'file': f}
        data = {
            'title': 'Balance Sheet 2024',
            'report_type': 'BALANCE_SHEET',
            'year': '2024'
        }
        response = requests.post(
            f"{base_url}/api/v1/documents/upload/",
            headers=headers,
            files=files,
            data=data
        )
        print("Balance Sheet Upload Response:", response.text)

    # Test Chargesheet Upload
    with open('test_data/chargesheet_2024.csv', 'rb') as f:
        files = {'file': f}
        data = {
            'title': 'Chargesheet 2024',
            'report_type': 'CHARGESHEET',
            'year': '2024'
        }
        response = requests.post(
            f"{base_url}/api/v1/documents/upload/",
            headers=headers,
            files=files,
            data=data
        )
        print("Chargesheet Upload Response:", response.text)

    # Process Documents
    response = requests.post(
        f"{base_url}/api/v1/documents/process/",
        headers=headers
    )
    print("Processing Response:", response.text)

if __name__ == "__main__":
    test_upload_and_process()
