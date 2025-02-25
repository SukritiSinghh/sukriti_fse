from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
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
