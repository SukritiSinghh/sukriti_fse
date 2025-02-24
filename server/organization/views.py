from django.shortcuts import render
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from authentication.models import Organization, User
from .models import FinancialDocument, BalanceSheetData
from .serializers import FinancialDocumentSerializer, BalanceSheetDataSerializer
import logging
import json
from .ai_processor import process_financial_document
from rest_framework.decorators import api_view, permission_classes
from .document_processor import process_pending_documents
import os
import uuid
import pandas as pd
from sklearn.ensemble import IsolationForest
from statsmodels.tsa.arima.model import ARIMA
import numpy as np
from django.db import connection

logger = logging.getLogger(__name__)

# Create your views here.

class FileUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            # Get the user's organization
            user = request.user
            logger.info(f"Processing upload request for user: {user.username}")
            logger.info(f"Request data: {request.data}")
            logger.info(f"Files: {request.FILES}")
            
            # Get organization from the request data
            org_name = request.data.get('organization')
            try:
                organization = Organization.objects.get(name=org_name)
            except Organization.DoesNotExist:
                logger.error(f"Organization not found: {org_name}")
                return Response({"error": f"Organization '{org_name}' not found"}, 
                             status=status.HTTP_404_NOT_FOUND)

            # Handle file upload
            file_obj = request.FILES.get('file')
            if not file_obj:
                logger.error("No file provided in request")
                return Response({"error": "No file provided"}, 
                             status=status.HTTP_400_BAD_REQUEST)

            logger.info(f"File details - Name: {file_obj.name}, Size: {file_obj.size}, Content Type: {file_obj.content_type}")

            # Create a unique filename
            file_extension = os.path.splitext(file_obj.name)[1]
            unique_filename = f"{uuid.uuid4()}{file_extension}"
            
            # Set the upload path
            upload_path = os.path.join('documents', org_name, str(request.data.get('year')))
            
            # Validate report type
            report_type = request.data.get('reportType', 'OTHER')
            if report_type not in dict(FinancialDocument.ReportType.CHOICES):
                logger.error(f"Invalid report type: {report_type}")
                return Response({"error": f"Invalid report type: {report_type}"}, 
                             status=status.HTTP_400_BAD_REQUEST)

            # Get year with validation
            try:
                year = int(request.data.get('year', 2024))
            except ValueError:
                logger.error(f"Invalid year format: {request.data.get('year')}")
                return Response({"error": "Invalid year format"}, 
                             status=status.HTTP_400_BAD_REQUEST)

            # Create document with the file field
            document = FinancialDocument(
                organization=organization,
                uploaded_by=request.data.get('uploaded_by', user.username),
                file_name=file_obj.name,
                title=request.data.get('title') or file_obj.name,
                report_type=report_type,
                year=year,
                status=FinancialDocument.Status.PENDING
            )
            
            # Save the file with a unique name in the correct directory
            document.file.save(
                os.path.join(upload_path, unique_filename),
                file_obj,
                save=False
            )
            
            # Save the document
            document.save()

            logger.info(f"Document created successfully with ID: {document.id}")
            logger.info(f"File saved at: {document.file.path}")

            return Response({
                "message": "File uploaded successfully",
                "document_id": document.id,
                "file_name": document.file_name,
                "file_path": document.file.url,
                "status": document.status,
                "organization": organization.name,
                "report_type": document.report_type,
                "year": document.year
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            logger.exception(f"Error in file upload: {str(e)}")
            return Response({
                "error": f"Error processing file upload: {str(e)}",
                "details": "Please check server logs for more information"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request, *args, **kwargs):
        try:
            org_name = request.query_params.get('organization')
            if not org_name:
                return Response(
                    {'error': 'Organization name is required'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            try:
                organization = Organization.objects.get(name=org_name)
            except Organization.DoesNotExist:
                return Response(
                    {'error': f'Organization with name {org_name} does not exist'},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            documents = FinancialDocument.objects.filter(organization=organization)
            serializer = FinancialDocumentSerializer(documents, many=True)
            return Response(serializer.data)
        
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class ProcessDocumentView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, document_id):
        try:
            # Get the document
            document = FinancialDocument.objects.get(id=document_id)
            
            # Process the document using AI
            result = process_financial_document(document)
            
            if not result:
                return Response(
                    {'error': 'Failed to process document'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Parse the JSON result from Gemini
            try:
                extracted_data = json.loads(result)
            except json.JSONDecodeError:
                return Response(
                    {'error': 'Invalid data format from AI processor'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Create or update BalanceSheetData
            balance_sheet_data, created = BalanceSheetData.objects.update_or_create(
                document=document,
                defaults={
                    'total_revenue': extracted_data.get('total_revenue'),
                    'total_expense': extracted_data.get('total_expense'),
                    'net_profit': extracted_data.get('net_profit'),
                    'assets': extracted_data.get('assets'),
                    'liabilities': extracted_data.get('liabilities'),
                    'equity': extracted_data.get('equity')
                }
            )
            
            serializer = BalanceSheetDataSerializer(balance_sheet_data)
            return Response(serializer.data, status=status.HTTP_200_OK)
            
        except FinancialDocument.DoesNotExist:
            return Response(
                {'error': 'Document not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.exception("Error processing document")
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def get(self, request, document_id):
        try:
            document = FinancialDocument.objects.get(id=document_id)
            balance_sheet_data = BalanceSheetData.objects.filter(document=document).first()
            
            if not balance_sheet_data:
                return Response(
                    {'error': 'No processed data found for this document'},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            serializer = BalanceSheetDataSerializer(balance_sheet_data)
            return Response(serializer.data, status=status.HTTP_200_OK)
            
        except FinancialDocument.DoesNotExist:
            return Response(
                {'error': 'Document not found'},
                status=status.HTTP_404_NOT_FOUND
            )

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def process_documents(request):
    try:
        result = process_pending_documents()
        return Response(result, status=status.HTTP_200_OK)
    except Exception as e:
        logger.error(f"Error processing documents: {str(e)}")
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class OrganizationViewSet(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # Extract data from request
            name = request.data.get('name')
            code = request.data.get('code')

            if not name:
                return Response({"error": "Organization name is required"}, 
                             status=status.HTTP_400_BAD_REQUEST)

            # Create the organization
            organization = Organization.objects.create(
                name=name,
                code=code if code else None  # If code is not provided, it will be auto-generated
            )

            # Associate the user with the organization
            user = request.user
            user.organization = organization
            user.save()

            return Response({
                "message": "Organization created successfully",
                "organization": {
                    "id": organization.id,
                    "name": organization.name,
                    "code": organization.code
                }
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            logger.exception(f"Error creating organization: {str(e)}")
            return Response({
                "error": "Failed to create organization",
                "details": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request):
        try:
            organizations = Organization.objects.all()
            data = [{
                "id": org.id,
                "name": org.name,
                "code": org.code
            } for org in organizations]
            return Response(data)
        except Exception as e:
            logger.exception(f"Error fetching organizations: {str(e)}")
            return Response({
                "error": "Failed to fetch organizations",
                "details": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class JoinOrganizationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            code = request.data.get('code')
            if not code:
                return Response({"error": "Organization code is required"}, 
                             status=status.HTTP_400_BAD_REQUEST)

            try:
                organization = Organization.objects.get(code=code)
            except Organization.DoesNotExist:
                return Response({"error": "Invalid organization code"}, 
                             status=status.HTTP_404_NOT_FOUND)

            # Associate the user with the organization
            user = request.user
            user.organization = organization
            user.save()

            return Response({
                "message": "Successfully joined organization",
                "organization": {
                    "id": organization.id,
                    "name": organization.name,
                    "code": organization.code
                }
            })

        except Exception as e:
            logger.exception(f"Error joining organization: {str(e)}")
            return Response({
                "error": "Failed to join organization",
                "details": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class FinancialDataView(APIView):
    def get_chargesheet_data(self, company_id: int, year: int):
        query = f"""
        SELECT * FROM chargesheets
        WHERE company_id = {company_id} AND year = {year}
        """
        with connection.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchall()
        return result

    def get_balance_sheet_data(self, company_id: int, year: int):
        query = f"""
        SELECT * FROM balance_sheets
        WHERE company_id = {company_id} AND year = {year}
        """
        with connection.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchall()
        return result

    def process_financial_data(self, raw_data):
        df = pd.DataFrame(raw_data)
        df.fillna(0, inplace=True)  # Handling missing values
        df['profit_margin'] = (df['revenue'] - df['expenses']) / df['revenue']
        return df

    def get_revenue_trend(self, company_id: int):
        query = f"""
        SELECT year, SUM(revenue) as total_revenue FROM balance_sheets
        WHERE company_id = {company_id} GROUP BY year ORDER BY year
        """
        with connection.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchall()
        return result

    def get_expense_trend(self, company_id: int):
        query = f"""
        SELECT year, SUM(expenses) as total_expenses FROM balance_sheets
        WHERE company_id = {company_id} GROUP BY year ORDER BY year
        """
        with connection.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchall()
        return result

    def detect_anomalies(self, financial_data):
        df = pd.DataFrame(financial_data)
        model = IsolationForest(contamination=0.05)  # 5% anomaly threshold
        df['anomaly'] = model.fit_predict(df[['revenue', 'expenses']])
        anomalies = df[df['anomaly'] == -1]
        return anomalies

    def forecast_revenue(self, company_id: int):
        query = f"""
        SELECT year, revenue FROM balance_sheets WHERE company_id = {company_id} ORDER BY year
        """
        with connection.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchall()
        df = pd.DataFrame(result, columns=["year", "revenue"])
        model = ARIMA(df["revenue"], order=(5,1,0))  # ARIMA model for forecasting
        model_fit = model.fit()
        future_years = np.arange(df["year"].max() + 1, df["year"].max() + 6)  # Predict next 5 years
        forecast = model_fit.forecast(steps=5)
        return list(zip(future_years, forecast))

    def get(self, request, company_id, year):
        chargesheet_data = self.get_chargesheet_data(company_id, year)
        balance_sheet_data = self.get_balance_sheet_data(company_id, year)
        processed_data = self.process_financial_data(balance_sheet_data)
        revenue_trend = self.get_revenue_trend(company_id)
        expense_trend = self.get_expense_trend(company_id)
        anomalies = self.detect_anomalies(processed_data)
        revenue_forecast = self.forecast_revenue(company_id)

        return Response({
            'chargesheet_data': chargesheet_data,
            'balance_sheet_data': balance_sheet_data,
            'revenue_trend': revenue_trend,
            'expense_trend': expense_trend,
            'anomalies': anomalies.to_dict(orient='records'),
            'revenue_forecast': revenue_forecast
        }, status=status.HTTP_200_OK)

@api_view(['GET'])
def api_get_chargesheet(request, company_id, year):
    view = FinancialDataView()
    data = view.get_chargesheet_data(company_id, year)
    return Response(data)

@api_view(['GET'])
def api_get_balance_sheet(request, company_id, year):
    view = FinancialDataView()
    data = view.get_balance_sheet_data(company_id, year)
    return Response(data)

@api_view(['GET'])
def api_get_revenue_trend(request, company_id):
    view = FinancialDataView()
    trend = view.get_revenue_trend(company_id)
    return Response(trend)

@api_view(['GET'])
def api_detect_anomalies(request, company_id):
    view = FinancialDataView()
    raw_data = view.get_balance_sheet_data(company_id, year=None)  # Fetch all years
    anomalies = view.detect_anomalies(raw_data)
    return Response(anomalies.to_dict(orient="records"))

@api_view(['GET'])
def api_forecast_revenue(request, company_id):
    view = FinancialDataView()
    forecast = view.forecast_revenue(company_id)
    return Response(forecast)
