from rest_framework import serializers
from .models import FinancialDocument, BalanceSheetData
from authentication.models import Organization, User

class FinancialDocumentSerializer(serializers.ModelSerializer):
    organization = serializers.PrimaryKeyRelatedField(queryset=Organization.objects.all())
    file = serializers.FileField(required=True)
    uploaded_by = serializers.CharField(required=True)  # Accept username as a string
    year = serializers.IntegerField(required=True)  # New field for the year
    reportType = serializers.CharField(required=True)  # Accept report type as a string

    class Meta:
        model = FinancialDocument
        fields = ['id', 'organization', 'file', 'file_name', 'uploaded_at', 'status', 'uploaded_by', 'year', 'reportType']
        read_only_fields = ['uploaded_at', 'status']

    def validate_year(self, value):
        if value <= 0:
            raise serializers.ValidationError("Year must be a positive integer.")
        return value

    def create(self, validated_data):
        print("Validated data:", validated_data)  # Debugging
        print("Validated data type:", type(validated_data))  # Debugging
        print("Validated data keys:", validated_data.keys())  # Debugging
        instance = super().create(validated_data)
        print("Document saved with ID:", instance.id)  # Debugging
        print("Saved instance:", instance)  # Debugging
        return instance

class BalanceSheetDataSerializer(serializers.ModelSerializer):
    document_name = serializers.CharField(source='document.file_name', read_only=True)
    
    class Meta:
        model = BalanceSheetData
        fields = ['id', 'document', 'document_name', 'total_revenue', 'total_expense', 
                 'net_profit', 'assets', 'liabilities', 'equity', 'processed_at']
        read_only_fields = ['processed_at']
