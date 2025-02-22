from django.core.management.base import BaseCommand
from authentication.models import Organization, User
from org.models import ChargeSheet, BalanceSheet, FinancialInsight

class Command(BaseCommand):
    help = 'Populate the database with dummy data'

    def handle(self, *args, **kwargs):
        # Create dummy organizations
        org1 = Organization.objects.create(name='Tech Corp', address='123 Tech Lane')
        org2 = Organization.objects.create(name='Finance Inc.', address='456 Finance Ave')
        org3 = Organization.objects.create(name='Health Solutions', address='789 Health Blvd')

        # Create dummy users
        user1 = User.objects.create_user(username='admin1', password='admin123', role='Admin', organization=org1)
        user2 = User.objects.create_user(username='finance_user1', password='finance123', role='Finance', organization=org1)
        user3 = User.objects.create_user(username='admin2', password='admin123', role='Admin', organization=org2)
        user4 = User.objects.create_user(username='finance_user2', password='finance123', role='Finance', organization=org2)
        user5 = User.objects.create_user(username='admin3', password='admin123', role='Admin', organization=org3)

        # Create dummy charge sheets
        ChargeSheet.objects.create(organization=org1, year=2025, total_revenue=100000, total_expenses=50000)
        ChargeSheet.objects.create(organization=org2, year=2025, total_revenue=200000, total_expenses=100000)
        ChargeSheet.objects.create(organization=org3, year=2025, total_revenue=150000, total_expenses=70000)

        # Create dummy balance sheets
        BalanceSheet.objects.create(organization=org1, year=2025, assets=150000, liabilities=30000)
        BalanceSheet.objects.create(organization=org2, year=2025, assets=250000, liabilities=50000)
        BalanceSheet.objects.create(organization=org3, year=2025, assets=180000, liabilities=45000)

        # Create dummy financial insights
        FinancialInsight.objects.create(organization=org1, year=2025, risk_score=20.5, fraud_alert=False, retention_probability=0.85)
        FinancialInsight.objects.create(organization=org2, year=2025, risk_score=15.0, fraud_alert=False, retention_probability=0.90)
        FinancialInsight.objects.create(organization=org3, year=2025, risk_score=10.0, fraud_alert=False, retention_probability=0.95)

        self.stdout.write(self.style.SUCCESS('Successfully populated the database with dummy data.'))
