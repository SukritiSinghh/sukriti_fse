from django.shortcuts import render
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Income, Expense, FinancialGoal
from .serializers import (
    IncomeSerializer, 
    ExpenseSerializer, 
    FinancialGoalSerializer
)

# Create your views here.

class FinancialRecordPermission(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit/view it
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any authenticated request
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated
        
        # Write permissions are only allowed to the owner of the record
        return obj.user == request.user

class IncomeViewSet(viewsets.ModelViewSet):
    """
    Viewset for managing income records
    """
    serializer_class = IncomeSerializer
    permission_classes = [permissions.IsAuthenticated, FinancialRecordPermission]
    
    def get_queryset(self):
        # Only return income records for the current user
        return Income.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        # Automatically set the user to the current user
        serializer.save(user=self.request.user)
    
    @action(detail=False, methods=['GET'])
    def summary(self, request):
        """
        Provide a summary of income records
        """
        queryset = self.get_queryset()
        total_income = sum(income.amount for income in queryset)
        income_types = {}
        
        for income in queryset:
            income_types[income.get_income_type_display()] = income_types.get(
                income.get_income_type_display(), 0
            ) + income.amount
        
        return Response({
            'total_income': total_income,
            'income_breakdown': income_types
        })

class ExpenseViewSet(viewsets.ModelViewSet):
    """
    Viewset for managing expense records
    """
    serializer_class = ExpenseSerializer
    permission_classes = [permissions.IsAuthenticated, FinancialRecordPermission]
    
    def get_queryset(self):
        # Only return expense records for the current user
        return Expense.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        # Automatically set the user to the current user
        serializer.save(user=self.request.user)
    
    @action(detail=False, methods=['GET'])
    def summary(self, request):
        """
        Provide a summary of expense records
        """
        queryset = self.get_queryset()
        total_expenses = sum(expense.amount for expense in queryset)
        expense_categories = {}
        
        for expense in queryset:
            expense_categories[expense.get_category_display()] = expense_categories.get(
                expense.get_category_display(), 0
            ) + expense.amount
        
        return Response({
            'total_expenses': total_expenses,
            'expense_breakdown': expense_categories
        })

class FinancialGoalViewSet(viewsets.ModelViewSet):
    """
    Viewset for managing financial goals
    """
    serializer_class = FinancialGoalSerializer
    permission_classes = [permissions.IsAuthenticated, FinancialRecordPermission]
    
    def get_queryset(self):
        # Only return financial goals for the current user
        return FinancialGoal.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        # Automatically set the user to the current user
        serializer.save(user=self.request.user)
    
    @action(detail=False, methods=['GET'])
    def progress_summary(self, request):
        """
        Provide a summary of financial goal progress
        """
        queryset = self.get_queryset()
        goals_summary = [{
            'name': goal.name,
            'target_amount': goal.target_amount,
            'current_amount': goal.current_amount,
            'progress_percentage': goal.progress_percentage()
        } for goal in queryset]
        
        return Response({
            'goals': goals_summary,
            'total_goals': len(queryset)
        })
