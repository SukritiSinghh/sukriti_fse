import pandas as pd
import os
from django.utils.dateparse import parse_date
from django.utils import timezone
from django.db import transaction
import logging
from .models import FinancialDocument, BalanceSheetData, ChargesheetData

logger = logging.getLogger(__name__)

def process_pending_documents():
    try:
        pending_documents = FinancialDocument.objects.filter(status=FinancialDocument.Status.PENDING)
        processed_data = []

        for document in pending_documents:
            try:
                # Ensure file exists
                if not os.path.exists(document.file.path):
                    raise FileNotFoundError(f"File not found: {document.file.path}")

                # Read file with proper encoding
                try:
                    df = pd.read_excel(document.file.path) if document.file.name.endswith(('.xlsx', '.xls')) else pd.read_csv(document.file.path)
                except Exception as e:
                    logger.error(f"Error reading file {document.file.path}: {str(e)}")
                    raise Exception(f"Error reading file: {str(e)}")

                # Normalize column names
                df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
                logger.info(f"Normalized columns: {list(df.columns)}")

                data = {}
                if document.report_type == FinancialDocument.ReportType.BALANCE_SHEET:
                    with transaction.atomic():
                        # Extract balance sheet data with defaults and error handling
                        try:
                            balance_sheet = BalanceSheetData.objects.create(
                                document=document,
                                total_revenue=float(df.get('total_revenue', pd.Series([0])).iloc[0] or 0),
                                total_expense=float(df.get('total_expense', pd.Series([0])).iloc[0] or 0),
                                net_profit=float(df.get('net_profit', pd.Series([0])).iloc[0] or 0),
                                assets=float(df.get('assets', pd.Series([0])).iloc[0] or 0),
                                liabilities=float(df.get('liabilities', pd.Series([0])).iloc[0] or 0),
                                equity=float(df.get('equity', pd.Series([0])).iloc[0] or 0),
                                processed_at=timezone.now()
                            )
                            
                            data = {
                                'type': 'balance_sheet',
                                'data': {
                                    'total_revenue': float(balance_sheet.total_revenue),
                                    'total_expense': float(balance_sheet.total_expense),
                                    'net_profit': float(balance_sheet.net_profit),
                                    'assets': float(balance_sheet.assets),
                                    'liabilities': float(balance_sheet.liabilities),
                                    'equity': float(balance_sheet.equity),
                                    'processed_at': balance_sheet.processed_at.isoformat()
                                }
                            }
                        except Exception as e:
                            logger.error(f"Error processing balance sheet data: {str(e)}")
                            raise Exception(f"Error processing balance sheet data: {str(e)}")

                elif document.report_type == FinancialDocument.ReportType.CHARGESHEET:
                    charges_data = []
                    with transaction.atomic():
                        for idx, row in df.iterrows():
                            try:
                                # Handle date with proper error handling
                                date = pd.to_datetime(row.get('date', timezone.now()), errors='coerce')
                                if pd.isna(date):
                                    date = timezone.now()
                                
                                # Create charge sheet entry with defaults
                                charge = ChargesheetData.objects.create(
                                    document=document,
                                    charges=str(row.get('charges', '')),
                                    date=date.date(),
                                    amount=float(row.get('amount', 0) or 0),
                                    processed_at=timezone.now()
                                )
                                
                                charges_data.append({
                                    'charges': charge.charges,
                                    'date': charge.date.isoformat(),
                                    'amount': float(charge.amount),
                                    'processed_at': charge.processed_at.isoformat()
                                })
                            except Exception as e:
                                logger.error(f"Error processing charge sheet row {idx}: {str(e)}")
                                continue  # Skip problematic rows but continue processing
                    
                    data = {
                        'type': 'chargesheet',
                        'data': charges_data
                    }

                # Update document status
                document.status = FinancialDocument.Status.PROCESSED
                document.save()
                
                processed_data.append({
                    'document_id': document.id,
                    'title': document.title,
                    'report_type': document.report_type,
                    'processed_data': data
                })

            except Exception as e:
                logger.error(f"Error processing document {document.id}: {str(e)}")
                document.status = FinancialDocument.Status.FAILED
                document.save()
                processed_data.append({
                    'document_id': document.id,
                    'title': document.title,
                    'report_type': document.report_type,
                    'error': str(e)
                })

        return {
            'message': 'Documents processed successfully',
            'processed_documents': processed_data
        }
    except Exception as e:
        logger.error(f"Error in process_pending_documents: {str(e)}")
        return {'error': str(e)}

def save_balance_sheet_data(df, document):
    """Extract and save balance sheet data."""
    try:
        # Normalize column names
        df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
        
        with transaction.atomic():
            balance_sheet_data = BalanceSheetData(
                document=document,
                total_revenue=float(df.get('total_revenue', pd.Series([0])).iloc[0] or 0),
                total_expense=float(df.get('total_expense', pd.Series([0])).iloc[0] or 0),
                net_profit=float(df.get('net_profit', pd.Series([0])).iloc[0] or 0),
                assets=float(df.get('assets', pd.Series([0])).iloc[0] or 0),
                liabilities=float(df.get('liabilities', pd.Series([0])).iloc[0] or 0),
                equity=float(df.get('equity', pd.Series([0])).iloc[0] or 0),
            )
            balance_sheet_data.save()
            return balance_sheet_data
    except Exception as e:
        logger.error(f"Error saving balance sheet data: {str(e)}")
        raise

def save_chargesheet_data(df, document):
    """Extract and save chargesheet data."""
    try:
        # Normalize column names
        df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
        
        charges_data = []
        with transaction.atomic():
            for idx, row in df.iterrows():
                try:
                    date = pd.to_datetime(row.get('date', timezone.now()), errors='coerce')
                    if pd.isna(date):
                        date = timezone.now()

                    charge_data = ChargesheetData.objects.create(
                        document=document,
                        charges=str(row.get('charges', '')),
                        date=date.date(),
                        amount=float(row.get('amount', 0) or 0),
                        processed_at=timezone.now()
                    )
                    charges_data.append(charge_data)
                except Exception as e:
                    logger.error(f"Error processing charge sheet row {idx}: {str(e)}")
                    continue
            
            return charges_data
    except Exception as e:
        logger.error(f"Error saving chargesheet data: {str(e)}")
        raise
