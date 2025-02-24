from django.db import models
from django.conf import settings
from datetime import datetime
import os

def financial_report_upload_path(instance, filename):
    """Organize files by year in the 'financial_reports' directory"""
    year = datetime.now().year
    return os.path.join('financial_reports', str(year), filename)

# Create your models here.

class FinancialRecord(models.Model):
    """
    Base model for tracking financial records
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='%(class)s_records'
    )
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        abstract = True
        ordering = ['-date']

class Income(FinancialRecord):
    """
    Model to track income sources
    """
    INCOME_TYPES = [
        ('SALARY', 'Salary'),
        ('INVESTMENT', 'Investment Returns'),
        ('FREELANCE', 'Freelance Work'),
        ('OTHER', 'Other Income')
    ]
    
    income_type = models.CharField(
        max_length=20, 
        choices=INCOME_TYPES, 
        default='OTHER'
    )

class Expense(FinancialRecord):
    """
    Model to track expenses
    """
    EXPENSE_CATEGORIES = [
        ('HOUSING', 'Housing'),
        ('TRANSPORT', 'Transportation'),
        ('FOOD', 'Food'),
        ('UTILITIES', 'Utilities'),
        ('ENTERTAINMENT', 'Entertainment'),
        ('OTHER', 'Other Expenses')
    ]
    
    category = models.CharField(
        max_length=20, 
        choices=EXPENSE_CATEGORIES, 
        default='OTHER'
    )
    is_recurring = models.BooleanField(default=False)

class Organization(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=10, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Generate a unique code if not set
        if not self.code:
            import random
            import string
            while True:
                code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
                if not Organization.objects.filter(code=code).exists():
                    self.code = code
                    break
        super().save(*args, **kwargs)

class User(models.Model):
    organization = models.ForeignKey(
        Organization, 
        on_delete=models.SET_NULL,  # Set to null when organization is deleted
        related_name='users',
        null=True,  # Allow null values
        blank=True  # Allow blank in forms
    )

    def __str__(self):
        return self.username

class FinancialGoal(models.Model):
    """
    Model to track financial goals
    """
    organization = models.ForeignKey(
        Organization, 
        on_delete=models.SET_NULL,
        related_name='financial_goals',
        null=True,
        blank=True
    )
    name = models.CharField(max_length=100)
    target_amount = models.DecimalField(max_digits=15, decimal_places=2)
    current_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    deadline = models.DateField()
    
    def progress_percentage(self):
        """Calculate goal progress percentage"""
        return (self.current_amount / self.target_amount) * 100 if self.target_amount > 0 else 0

    def __str__(self):
        return f"{self.name} - {self.progress_percentage():.2f}% complete"


class FinancialReport(models.Model):
    """Model for uploading and storing financial reports"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='financial_reports'
    )
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name='financial_reports'
    )
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to=financial_report_upload_path)
    description = models.TextField(blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    report_type = models.CharField(
        max_length=20,
        choices=[
            ('INCOME', 'Income Report'),
            ('EXPENSE', 'Expense Report'),
            ('BUDGET', 'Budget Plan'),
            ('TAX', 'Tax Document'),
            ('OTHER', 'Other')
        ],
        default='OTHER'
    )
    year = models.IntegerField()  # New field for the year
    upload_date = models.DateTimeField(auto_now_add=True)  # New field for the upload date

    class Meta:
        ordering = ['-uploaded_at']

    def __str__(self):
        return f"{self.title} - {self.uploaded_at.strftime('%Y-%m-%d')}"

    def filename(self):
        return os.path.basename(self.file.name)
