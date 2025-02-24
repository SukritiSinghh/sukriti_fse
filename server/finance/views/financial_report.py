from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from ..models import FinancialReport
from ..serializers import FinancialReportSerializer

class FinancialReportViewSet(viewsets.ModelViewSet):
    """ViewSet for Financial Reports"""
    serializer_class = FinancialReportSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return FinancialReport.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user,
            organization=self.request.user.organization
        )
