from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from ..models import Income
from ..serializers import IncomeSerializer

class IncomeViewSet(viewsets.ModelViewSet):
    """ViewSet for Income records"""
    serializer_class = IncomeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Income.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
