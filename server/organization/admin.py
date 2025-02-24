from django.contrib import admin
from .models import Organization, FinancialDocument, BalanceSheetData

# Register your models here.

@admin.register(FinancialDocument)
class FinancialDocumentAdmin(admin.ModelAdmin):
    list_display = ('id', 'organization', 'file_name', 'uploaded_by', 'uploaded_at', 'status', 'reportType', 'year')
    list_filter = ('status', 'reportType', 'year')
    search_fields = ('file_name', 'uploaded_by')
    ordering = ('-uploaded_at',)

@admin.register(BalanceSheetData)
class BalanceSheetDataAdmin(admin.ModelAdmin):
    list_display = ('document', 'total_revenue', 'total_expense', 'net_profit', 'processed_at')
    list_filter = ('processed_at',)
    search_fields = ('document__file_name',)
    ordering = ('-processed_at',)
