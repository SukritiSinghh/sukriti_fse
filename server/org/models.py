from django.db import models
from authentication.models import Organization

class ChargeSheet(models.Model):
    organization = models.ForeignKey(
        Organization, 
        on_delete=models.CASCADE,
        related_name='charge_sheets'
    )
    year = models.IntegerField()
    total_revenue = models.DecimalField(max_digits=15, decimal_places=2)
    total_expenses = models.DecimalField(max_digits=15, decimal_places=2)
    net_profit = models.DecimalField(max_digits=15, decimal_places=2)

    class Meta:
        verbose_name = 'Charge Sheet'
        verbose_name_plural = 'Charge Sheets'
        unique_together = ('organization', 'year')

    def __str__(self):
        return f"{self.organization.name} - {self.year} Charge Sheet"

    def save(self, *args, **kwargs):
        # Calculate net profit before saving
        self.net_profit = self.total_revenue - self.total_expenses
        super().save(*args, **kwargs)

class BalanceSheet(models.Model):
    organization = models.ForeignKey(
        Organization, 
        on_delete=models.CASCADE,
        related_name='balance_sheets'
    )
    year = models.IntegerField()
    assets = models.DecimalField(max_digits=15, decimal_places=2)
    liabilities = models.DecimalField(max_digits=15, decimal_places=2)
    equity = models.DecimalField(max_digits=15, decimal_places=2)

    class Meta:
        verbose_name = 'Balance Sheet'
        verbose_name_plural = 'Balance Sheets'
        unique_together = ('organization', 'year')

    def __str__(self):
        return f"{self.organization.name} - {self.year} Balance Sheet"

    def save(self, *args, **kwargs):
        # Ensure accounting equation: Assets = Liabilities + Equity
        self.equity = self.assets - self.liabilities
        super().save(*args, **kwargs)

class FinancialInsight(models.Model):
    organization = models.ForeignKey(
        Organization, 
        on_delete=models.CASCADE,
        related_name='financial_insights'
    )
    year = models.IntegerField()
    risk_score = models.FloatField(
        help_text='Risk score from 0 to 100'
    )
    fraud_alert = models.BooleanField(default=False)
    retention_probability = models.FloatField(
        help_text='Probability of client retention (0 to 1)'
    )

    class Meta:
        verbose_name = 'Financial Insight'
        verbose_name_plural = 'Financial Insights'
        unique_together = ('organization', 'year')

    def __str__(self):
        return f"{self.organization.name} - {self.year} Financial Insight"

    def clean(self):
        # Validate score ranges
        if not 0 <= self.risk_score <= 100:
            raise models.ValidationError('Risk score must be between 0 and 100')
        if not 0 <= self.retention_probability <= 1:
            raise models.ValidationError('Retention probability must be between 0 and 1')
