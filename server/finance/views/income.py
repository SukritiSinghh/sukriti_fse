from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum
from django.utils import timezone
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

    @action(detail=False, methods=['get'])
    def summary(self, request):
        """Return a summary of income for different time periods."""
        today = timezone.localtime().date()
        month_start = today.replace(day=1)
        year_start = today.replace(month=1, day=1)

        # Convert dates to datetime with timezone
        today_start = timezone.make_aware(timezone.datetime.combine(today, timezone.datetime.min.time()))
        today_end = timezone.make_aware(timezone.datetime.combine(today, timezone.datetime.max.time()))

        income_data = {
            'today': self.get_queryset().filter(date__range=(today_start, today_end)).aggregate(total=Sum('amount'))['total'] or 0,
            'this_month': self.get_queryset().filter(date__gte=month_start).aggregate(total=Sum('amount'))['total'] or 0,
            'this_year': self.get_queryset().filter(date__gte=year_start).aggregate(total=Sum('amount'))['total'] or 0,
        }
        return Response(income_data)
