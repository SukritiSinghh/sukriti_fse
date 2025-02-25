from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from ..models import FinancialGoal
from ..serializers import FinancialGoalSerializer

class FinancialGoalViewSet(viewsets.ModelViewSet):
    """ViewSet for Financial Goals"""
    serializer_class = FinancialGoalSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return FinancialGoal.objects.filter(organization=self.request.user.organization)

    def perform_create(self, serializer):
        serializer.save(organization=self.request.user.organization)

    @action(detail=False, methods=['get'])
    def progress_summary(self, request):
        """Get progress summary of all goals"""
        goals = self.get_queryset()
        summary = []
        for goal in goals:
            progress = (goal.current_amount / goal.target_amount) * 100
            summary.append({
                'id': goal.id,
                'name': goal.name,
                'target_amount': goal.target_amount,
                'current_amount': goal.current_amount,
                'progress_percentage': round(progress, 2),
                'deadline': goal.deadline
            })
        return Response(summary)
