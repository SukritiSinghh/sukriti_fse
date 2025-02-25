from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from finance.models import FinancialReport, Organization
from django.core.files.uploadedfile import SimpleUploadedFile
import os
from datetime import datetime

User = get_user_model()

class FinancialReportTests(TestCase):
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

        # Create a test file
        self.test_file = SimpleUploadedFile(
            "test_report.pdf",
            b"file_content",
            content_type="application/pdf"
        )

    def test_upload_report(self):
        """Test uploading a simple financial report"""
        data = {
            'title': 'Q1 Financial Report',
            'file': self.test_file,
            'description': 'Financial report for Q1',
            'report_type': 'INCOME',
            'organization': self.organization.id,
            'year': datetime.now().year
        }
        response = self.client.post('/api/v1/finance/reports/', data, format='multipart')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['title'], 'Q1 Financial Report')
        self.assertEqual(response.data['report_type'], 'INCOME')

    def test_list_reports(self):
        """Test listing financial reports"""
        # Clear any existing reports to ensure only one is created
        FinancialReport.objects.all().delete()  # Clear any existing reports
        FinancialReport.objects.create(
            user=self.user,
            organization=self.organization,
            title='Test Report',
            file=self.test_file,
            report_type='INCOME',
            year=datetime.now().year
        )
        
        response = self.client.get('/api/v1/finance/reports/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
