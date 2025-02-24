from django.db import models
from authentication.models import Organization

# Create your models here.

class FinancialDocument(models.Model):
    class Status:
        PENDING = 'PENDING'
        PROCESSED = 'PROCESSED'
        FAILED = 'FAILED'

        CHOICES = [
            (PENDING, 'Pending'),
            (PROCESSED, 'Processed'),
            (FAILED, 'Failed')
        ]

    class ReportType:
        OTHER = 'OTHER'
        BALANCE_SHEET = 'BALANCE_SHEET'
        CHARGESHEET = 'CHARGESHEET'

        CHOICES = [
            (OTHER, 'Other'),
            (BALANCE_SHEET, 'Balance Sheet'),
            (CHARGESHEET, 'Charge Sheet')
        ]

    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    uploaded_by = models.CharField(max_length=255)  # Store username as a string
    file = models.FileField(upload_to="uploads/")
    file_name = models.CharField(max_length=255, default='')  # Field to store the name of the uploaded file
    title = models.CharField(max_length=255, default='Untitled Document')  # Title of the document
    uploaded_at = models.DateTimeField(auto_now_add=True)
    year = models.PositiveIntegerField(default=2023)  # Set a default year
    report_type = models.CharField(max_length=50, choices=ReportType.CHOICES, default=ReportType.OTHER)
    status = models.CharField(max_length=20, choices=Status.CHOICES, default=Status.PENDING)

    def __str__(self):
        return f"{self.organization.name} - {self.title} ({self.uploaded_at})"

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

class ChargesheetData(models.Model):
    document = models.ForeignKey(FinancialDocument, on_delete=models.CASCADE, related_name='chargesheets')
    charges = models.TextField()  # Details about the charges
    date = models.DateField()  # Date of the chargesheet
    amount = models.DecimalField(max_digits=15, decimal_places=2)  # Total amount
    processed_at = models.DateTimeField(auto_now_add=True)  # Timestamp for processing

    class Meta:
        verbose_name = 'Chargesheet Data'
        verbose_name_plural = 'Chargesheet Data'
        ordering = ['-processed_at']

    def __str__(self):
        return f"Chargesheet for {self.document.file_name} on {self.date}"
