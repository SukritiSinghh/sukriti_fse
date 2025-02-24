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

logger = logging.getLogger(__name__)

# Create your views here.

class FileUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            # Check if this is a save operation
            if request.path.endswith('/save/'):
                # Create the document with the specific data
                document_data = {
                    "organization_id": 15,
                    "file": "/media/uploads/dummy_balance_sheet.xlsx",
                    "file_name": "dummy_balance_sheet.xlsx",
                    "uploaded_at": "2025-02-24T07:29:11.244556Z",
                    "reportType": "INCOME",
                    "status": "pending",
                    "uploaded_by": "admin",
                    "year": 2021
                }
                
                # Create and save the document
                document = FinancialDocument.objects.create(**document_data)
                print("Document created with ID:", document.id)
                
                # Return the response
                return Response({
                    "message": "Document saved successfully",
                    "document_id": document.id
                }, status=status.HTTP_201_CREATED)
            
            # If not a save operation, handle regular file upload
            # Log request data
            logger.info(f"Request data: {request.data}")
            logger.info(f"Files: {request.FILES}")
            
            # Get organization name from request data
            org_name = request.data.get('organization')
            logger.info(f"Organization name from request: {org_name}")
            
            if not org_name:
                return Response(
                    {'error': 'Organization name is required'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Get the organization by name
            try:
                organization = Organization.objects.get(name=org_name)
                logger.info(f"Found organization: {organization}")
            except Organization.DoesNotExist:
                logger.error(f"Organization not found: {org_name}")
                return Response(
                    {'error': f'Organization with name {org_name} does not exist'},
                    status=status.HTTP_404_NOT_FOUND
                )

            # Create a mutable copy of the data
            data = request.data.copy()
            data['organization'] = organization.id
            
            # Get the original filename from the uploaded file
            if 'file' in request.FILES:
                data['file_name'] = request.FILES['file'].name
            
            logger.info(f"Prepared data for serializer: {data}")

            # Create serializer with context
            file_serializer = FinancialDocumentSerializer(
                data=data,
                context={'user': request.user}
            )
            
            if file_serializer.is_valid():
                logger.info("Serializer is valid")
                file_serializer.save()
                print("Successfully saved:", file_serializer.instance)
                return Response(file_serializer.data, status=status.HTTP_201_CREATED)
            else:
                logger.error(f"Serializer errors: {file_serializer.errors}")
                return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            logger.exception("Error in file upload")
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

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
