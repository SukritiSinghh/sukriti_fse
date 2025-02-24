from django.db import models
from authentication.models import Organization, User

# Create your models here.

class FinancialDocument(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('PROCESSED', 'Processed'),
        ('FAILED', 'Failed')
    ]
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    uploaded_by = models.CharField(max_length=255)  # Store username as a string
    file = models.FileField(upload_to="uploads/")
    file_name = models.CharField(max_length=255, default='')  # Field to store the name of the uploaded file
    uploaded_at = models.DateTimeField(auto_now_add=True)
    year = models.PositiveIntegerField(default=2023)  # Set a default year
    reportType = models.CharField(max_length=50, default='OTHER')  # Field to store the type of report
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')

    def __str__(self):
        return f"{self.organization.name} - {self.uploaded_at}"

    class Meta:
        ordering = ['-uploaded_at']

class BalanceSheetData(models.Model):
    document = models.ForeignKey(FinancialDocument, on_delete=models.CASCADE, related_name='extracted_data')
    total_revenue = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    total_expense = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    net_profit = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    assets = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    liabilities = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    equity = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    processed_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Balance Sheet Data'
        verbose_name_plural = 'Balance Sheet Data'
        ordering = ['-processed_at']
    
    def __str__(self):
        return f"Financial Data for {self.document.file_name}"
