from django.contrib import admin
from .models import Organization, FinancialDocument, BalanceSheetData, ChargesheetData

# Register your models here.

@admin.register(FinancialDocument)
class FinancialDocumentAdmin(admin.ModelAdmin):
    list_display = ('id', 'organization', 'uploaded_by', 'file_name', 'title', 'year', 'report_type', 'status', 'uploaded_at')
    list_filter = ('status', 'report_type', 'organization', 'year')
    search_fields = ('file_name', 'uploaded_by', 'organization__name')
    ordering = ('-uploaded_at',)

@admin.register(BalanceSheetData)
class BalanceSheetDataAdmin(admin.ModelAdmin):
    list_display = ('document', 'total_revenue', 'total_expense', 'net_profit', 'processed_at')
    list_filter = ('processed_at',)
    search_fields = ('document__file_name',)
    ordering = ('-processed_at',)

@admin.register(ChargesheetData)
class ChargesheetDataAdmin(admin.ModelAdmin):
    list_display = ('document', 'charges', 'date', 'amount', 'processed_at')
    list_filter = ('date', 'processed_at')
    search_fields = ('document__file_name', 'charges')
    ordering = ('-processed_at',)
