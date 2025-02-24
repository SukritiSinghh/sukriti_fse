from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from ..models import FinancialGoal
from ..serializers import FinancialGoalSerializer

class FinancialGoalViewSet(viewsets.ModelViewSet):
    """ViewSet for Financial Goals"""
    serializer_class = FinancialGoalSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return FinancialGoal.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
