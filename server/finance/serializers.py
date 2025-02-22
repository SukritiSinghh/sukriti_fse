from rest_framework import serializers
from .models import Income, Expense, FinancialGoal

class IncomeSerializer(serializers.ModelSerializer):
    """
    Serializer for Income records
    """
    class Meta:
        model = Income
        fields = ['id', 'user', 'amount', 'description', 'date', 'income_type']
        read_only_fields = ['user', 'date']

class ExpenseSerializer(serializers.ModelSerializer):
    """
    Serializer for Expense records
    """
    class Meta:
        model = Expense
        fields = ['id', 'user', 'amount', 'description', 'date', 'category', 'is_recurring']
        read_only_fields = ['user', 'date']

class FinancialGoalSerializer(serializers.ModelSerializer):
    """
    Serializer for Financial Goals
    """
    progress_percentage = serializers.SerializerMethodField()

    class Meta:
        model = FinancialGoal
        fields = [
            'id', 
            'user', 
            'name', 
            'target_amount', 
            'current_amount', 
            'deadline', 
            'progress_percentage'
        ]
        read_only_fields = ['user', 'progress_percentage']

    def get_progress_percentage(self, obj):
        return obj.progress_percentage()
