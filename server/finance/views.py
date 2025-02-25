from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum
from datetime import datetime, timedelta

from .models import Income, Expense, FinancialGoal, FinancialReport
from .serializers import (
    IncomeSerializer, ExpenseSerializer,
    FinancialGoalSerializer, FinancialReportSerializer
)

class IncomeViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing income records.
    """
    serializer_class = IncomeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        This view should return a list of all incomes
        for the currently authenticated user.
        """
        return Income.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """Save the post data when creating a new income."""
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'])
    def summary(self, request):
        """
        Return a summary of income for different time periods.
        """
        today = datetime.now().date()
        month_start = today.replace(day=1)
        year_start = today.replace(month=1, day=1)

        income_data = {
            'today': self.get_queryset().filter(date=today).aggregate(total=Sum('amount'))['total'] or 0,
            'this_month': self.get_queryset().filter(date__gte=month_start).aggregate(total=Sum('amount'))['total'] or 0,
            'this_year': self.get_queryset().filter(date__gte=year_start).aggregate(total=Sum('amount'))['total'] or 0,
        }
        return Response(income_data)

class ExpenseViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing expense records.
    """
    serializer_class = ExpenseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        This view should return a list of all expenses
        for the currently authenticated user.
        """
        return Expense.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """Save the post data when creating a new expense."""
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'])
    def summary(self, request):
        """
        Return a summary of expenses for different time periods.
        """
        today = datetime.now().date()
        month_start = today.replace(day=1)
        year_start = today.replace(month=1, day=1)

        expense_data = {
            'today': self.get_queryset().filter(date=today).aggregate(total=Sum('amount'))['total'] or 0,
            'this_month': self.get_queryset().filter(date__gte=month_start).aggregate(total=Sum('amount'))['total'] or 0,
            'this_year': self.get_queryset().filter(date__gte=year_start).aggregate(total=Sum('amount'))['total'] or 0,
        }
        return Response(expense_data)

class FinancialGoalViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing financial goals.
    """
    serializer_class = FinancialGoalSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        This view should return a list of all goals
        for the currently authenticated user.
        """
        return FinancialGoal.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """Save the post data when creating a new goal."""
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'])
    def progress_summary(self, request):
        """
        Return a summary of progress towards financial goals.
        """
        goals = self.get_queryset()
        goal_data = []
        for goal in goals:
            progress = (goal.current_amount / goal.target_amount) * 100 if goal.target_amount > 0 else 0
            goal_data.append({
                'id': goal.id,
                'title': goal.title,
                'target_amount': goal.target_amount,
                'current_amount': goal.current_amount,
                'progress_percentage': round(progress, 2)
            })
        return Response(goal_data)

class FinancialReportViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing financial reports.
    """
    serializer_class = FinancialReportSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        This view should return a list of all reports
        for the currently authenticated user.
        """
        return FinancialReport.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """Save the post data when creating a new report."""
        serializer.save(user=self.request.user)
