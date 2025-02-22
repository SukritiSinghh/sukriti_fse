from django.contrib import admin
from .models import ChargeSheet, BalanceSheet, FinancialInsight

# Register your models here.
admin.site.register(ChargeSheet)
admin.site.register(BalanceSheet)
admin.site.register(FinancialInsight)
