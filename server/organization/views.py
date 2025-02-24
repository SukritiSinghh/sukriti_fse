from django.shortcuts import render
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from authentication.models import Organization, User
from .models import FinancialDocument, BalanceSheetData, ChargesheetData
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
from django.db.models import Sum, Avg, Count, F, Q

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
    def get_chargesheet_data(self):
        try:
            chargesheet_data = ChargesheetData.objects.all().values(
                'id',
                'document_id',
                'charges',
                'date',
                'amount',
                'processed_at',
                'document__file_name',
                'document__title',
                'document__uploaded_by',
                'document__uploaded_at',
                'document__year'
            )
            return list(chargesheet_data)
        except Exception as e:
            logger.error(f"Error fetching chargesheet data: {str(e)}")
            return []

    def get_balance_sheet_data(self):
        try:
            balance_sheet_data = BalanceSheetData.objects.all().values(
                'id',
                'document_id',
                'total_revenue',
                'total_expense',
                'net_profit',
                'assets',
                'liabilities',
                'equity',
                'processed_at',
                'document__file_name',
                'document__title',
                'document__uploaded_by',
                'document__uploaded_at',
                'document__year'
            )
            return list(balance_sheet_data)
        except Exception as e:
            logger.error(f"Error fetching balance sheet data: {str(e)}")
            return []

    def process_financial_data(self, raw_data):
        try:
            df = pd.DataFrame(raw_data)
            df.fillna(0, inplace=True)
            
            # Calculate additional metrics
            if not df.empty and all(field in df.columns for field in ['total_revenue', 'total_expense']):
                df['profit_margin'] = ((df['total_revenue'] - df['total_expense']) / df['total_revenue']) * 100
                df['current_ratio'] = df['assets'] / df['liabilities'] if 'assets' in df.columns and 'liabilities' in df.columns else 0
                df['debt_to_equity'] = df['liabilities'] / df['equity'] if 'liabilities' in df.columns and 'equity' in df.columns else 0
            
            return df
        except Exception as e:
            logger.error(f"Error processing financial data: {str(e)}")
            return pd.DataFrame()

    def get_revenue_trend(self):
        try:
            revenue_data = BalanceSheetData.objects.values(
                'document__year'
            ).annotate(
                total_revenue=Sum('total_revenue')
            ).order_by('document__year')
            
            return list(revenue_data)
        except Exception as e:
            logger.error(f"Error fetching revenue trend: {str(e)}")
            return []

    def get_expense_trend(self):
        try:
            expense_data = BalanceSheetData.objects.values(
                'document__year'
            ).annotate(
                total_expense=Sum('total_expense')
            ).order_by('document__year')
            
            return list(expense_data)
        except Exception as e:
            logger.error(f"Error fetching expense trend: {str(e)}")
            return []

    def detect_anomalies(self, financial_data):
        try:
            df = pd.DataFrame(financial_data)
            if df.empty:
                return pd.DataFrame()
                
            # Select numerical columns for anomaly detection
            numeric_columns = ['total_revenue', 'total_expense', 'net_profit', 'assets', 'liabilities', 'equity']
            df_numeric = df[numeric_columns].fillna(0)
            
            if len(df_numeric) > 1:  # Need at least 2 data points for anomaly detection
                model = IsolationForest(contamination=0.05)
                df['anomaly'] = model.fit_predict(df_numeric)
                return df[df['anomaly'] == -1]
            return pd.DataFrame()
        except Exception as e:
            logger.error(f"Error detecting anomalies: {str(e)}")
            return pd.DataFrame()

    def forecast_revenue(self):
        try:
            # Get historical revenue data
            revenue_data = list(BalanceSheetData.objects.values(
                'document__year',
                'total_revenue'
            ).order_by('document__year'))
            
            if not revenue_data:
                logger.warning("No revenue data available for forecasting")
                return []
            
            # Convert to pandas DataFrame and ensure numeric types
            df = pd.DataFrame(revenue_data)
            
            # Convert and clean data
            df['document__year'] = df['document__year'].astype(int)
            df['total_revenue'] = df['total_revenue'].astype(float)
            
            # Drop any rows with missing values
            df = df.dropna()
            
            if len(df) < 3:
                logger.warning(f"Insufficient data points for forecasting. Need at least 3, got {len(df)}")
                return []
            
            try:
                # Create date range for the time series
                min_year = df['document__year'].min()
                date_range = pd.date_range(
                    start=f"{min_year}-01-01",
                    periods=len(df),
                    freq='Y'
                )
                
                # Create time series with proper index
                revenue_series = pd.Series(
                    data=df['total_revenue'].values,
                    index=date_range
                )
                
                # Make the series stationary by taking first difference
                revenue_diff = revenue_series.diff().dropna()
                
                if len(revenue_diff) < 2:
                    logger.warning("Insufficient data points after differencing")
                    return []
                
                # Fit ARIMA model with stationary data
                model = ARIMA(revenue_series, order=(1,1,0), enforce_stationarity=False)
                model_fit = model.fit()
                
                # Generate forecast
                last_year = int(df['document__year'].max())
                future_years = list(range(last_year + 1, last_year + 6))
                
                # Get forecast values using iloc for positional indexing
                forecast_values = model_fit.forecast(steps=5)
                
                # Create forecast pairs with proper types
                forecast_pairs = []
                for year, forecast_value in zip(future_years, forecast_values):
                    try:
                        value = float(forecast_value)
                        # Ensure forecast value is positive and not anomalous
                        if value > 0 and not (np.isnan(value) or np.isinf(value)):
                            forecast_pairs.append((year, value))
                    except (ValueError, TypeError) as e:
                        logger.error(f"Error processing forecast for year {year}: {str(e)}")
                        continue
                
                return forecast_pairs
                
            except Exception as e:
                logger.error(f"Error in ARIMA modeling: {str(e)}")
                return []
                
        except Exception as e:
            logger.error(f"Error in revenue forecasting: {str(e)}")
            return []

    def get(self, request):
        try:
            # Fetch all data without filtering by organization or year
            chargesheet_data = self.get_chargesheet_data()
            balance_sheet_data = self.get_balance_sheet_data()
            
            processed_data = self.process_financial_data(balance_sheet_data)
            revenue_trend = self.get_revenue_trend()
            expense_trend = self.get_expense_trend()
            anomalies = self.detect_anomalies(processed_data)
            
            try:
                revenue_forecast = self.forecast_revenue()
            except Exception as e:
                logger.error(f"Error in revenue forecasting, skipping: {str(e)}")
                revenue_forecast = []

            # Calculate overall statistics
            total_revenue = sum(float(d.get('total_revenue', 0) or 0) for d in balance_sheet_data)
            total_expense = sum(float(d.get('total_expense', 0) or 0) for d in balance_sheet_data)
            total_profit = total_revenue - total_expense
            
            latest_update = None
            if balance_sheet_data or chargesheet_data:
                all_dates = [d.get('processed_at') for d in balance_sheet_data + chargesheet_data if d.get('processed_at')]
                if all_dates:
                    latest_update = max(all_dates)
            
            response_data = {
                'chargesheet_data': chargesheet_data,
                'balance_sheet_data': balance_sheet_data,
                'revenue_trend': revenue_trend,
                'expense_trend': expense_trend,
                'anomalies': anomalies.to_dict(orient='records') if not anomalies.empty else [],
                'revenue_forecast': revenue_forecast,
                'summary_metrics': {
                    'total_documents': len(chargesheet_data) + len(balance_sheet_data),
                    'total_revenue': total_revenue,
                    'total_expense': total_expense,
                    'total_profit': total_profit,
                    'latest_update': latest_update,
                }
            }

            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error in FinancialDataView: {str(e)}")
            return Response({
                'error': 'Failed to fetch financial data',
                'details': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def api_get_chargesheet(request, company_id, year):
    view = FinancialDataView()
    data = view.get_chargesheet_data()
    return Response(data)

@api_view(['GET'])
def api_get_balance_sheet(request, company_id, year):
    view = FinancialDataView()
    data = view.get_balance_sheet_data()
    return Response(data)

@api_view(['GET'])
def api_get_revenue_trend(request, company_id):
    view = FinancialDataView()
    trend = view.get_revenue_trend()
    return Response(trend)

@api_view(['GET'])
def api_detect_anomalies(request, company_id):
    view = FinancialDataView()
    raw_data = view.get_balance_sheet_data()  # Fetch all years
    anomalies = view.detect_anomalies(raw_data)
    return Response(anomalies.to_dict(orient="records"))

@api_view(['GET'])
def api_forecast_revenue(request, company_id):
    view = FinancialDataView()
    forecast = view.forecast_revenue()
    return Response(forecast)
