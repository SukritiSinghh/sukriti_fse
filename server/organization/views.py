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

logger = logging.getLogger(__name__)

# Create your views here.

class FileUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            # Get the user's organization
            user = request.user
            logger.info(f"User: {user}, Organization: {getattr(user, 'organization', None)}")
            
            organization = user.organization
            if not organization:
                return Response({"error": "User is not associated with any organization"}, 
                             status=status.HTTP_400_BAD_REQUEST)

            # Handle file upload
            file_obj = request.FILES.get('file')
            if not file_obj:
                return Response({"error": "No file provided"}, 
                             status=status.HTTP_400_BAD_REQUEST)

            # Create document
            document = FinancialDocument.objects.create(
                organization=organization,
                uploaded_by=request.user.username,
                file=file_obj,
                file_name=file_obj.name,
                title=request.data.get('title', 'Untitled Document'),
                report_type=request.data.get('report_type', 'OTHER'),
                year=request.data.get('year', 2024),
                status=FinancialDocument.Status.PENDING
            )

            return Response({
                "message": "File uploaded successfully",
                "document_id": document.id,
                "file_name": document.file_name,
                "status": document.status
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            logger.error(f"Error in file upload: {str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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
