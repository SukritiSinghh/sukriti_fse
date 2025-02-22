from django.contrib import admin
from .models import Income, Expense, FinancialGoal

admin.site.register(Income)
admin.site.register(Expense)
admin.site.register(FinancialGoal)
