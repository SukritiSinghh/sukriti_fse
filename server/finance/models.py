from django.db import models
from django.conf import settings

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

class FinancialGoal(models.Model):
    """
    Model to track financial goals
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='financial_goals'
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
