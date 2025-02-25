from rest_framework import serializers
from .models import Income, Expense, FinancialGoal, FinancialReport, Organization

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
    """Serializer for Financial Goals"""
    progress_percentage = serializers.SerializerMethodField()

    class Meta:
        model = FinancialGoal
        fields = [
            'id', 
            'name', 
            'target_amount', 
            'current_amount', 
            'deadline', 
            'progress_percentage'
        ]
        read_only_fields = ['progress_percentage']

    def get_progress_percentage(self, obj):
        return obj.progress_percentage()


class OrganizationSerializer(serializers.ModelSerializer):
    """Serializer for Organizations"""
    class Meta:
        model = Organization
        fields = ['id', 'name', 'code', 'description', 'created_at', 'updated_at']
        read_only_fields = ['code', 'created_at', 'updated_at']


class FinancialReportSerializer(serializers.ModelSerializer):
    """Serializer for Financial Reports"""
    filename = serializers.SerializerMethodField()

    class Meta:
        model = FinancialReport
        fields = [
            'id',
            'user',
            'organization',
            'title',
            'file',
            'description',
            'uploaded_at',
            'report_type',
            'year',
            'upload_date',
            'filename'
        ]
        read_only_fields = ['user', 'organization', 'uploaded_at', 'upload_date', 'filename']

    def get_filename(self, obj):
        return obj.filename()

    def create(self, validated_data):
        # Get the user's organization
        user = self.context['request'].user
        validated_data['organization'] = user.organization
        validated_data['user'] = user
        return super().create(validated_data)
