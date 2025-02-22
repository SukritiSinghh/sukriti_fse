from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import IncomeViewSet, ExpenseViewSet, FinancialGoalViewSet

# Create a router and register viewsets
router = DefaultRouter()
router.register(r'income', IncomeViewSet, basename='income')
router.register(r'expenses', ExpenseViewSet, basename='expense')
router.register(r'goals', FinancialGoalViewSet, basename='financial-goal')

urlpatterns = [
    # Include router URLs
    path('', include(router.urls)),
    
    # Additional custom routes can be added here
    path('income/summary/', IncomeViewSet.as_view({'get': 'summary'}), name='income-summary'),
    path('expenses/summary/', ExpenseViewSet.as_view({'get': 'summary'}), name='expense-summary'),
    path('goals/progress/', FinancialGoalViewSet.as_view({'get': 'progress_summary'}), name='goals-progress'),
]
