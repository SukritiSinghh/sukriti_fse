import google.generativeai as genai
import fitz  # PyMuPDF
import pandas as pd
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

def configure_genai():
    """Configure Google Generative AI with API key"""
    try:
        genai.configure(api_key=settings.GENAI_API_KEY)
        return True
    except Exception as e:
        logger.error(f"Failed to configure Gemini AI: {str(e)}")
        return False

def extract_text_from_pdf(pdf_path):
    """Extract text from PDF using PyMuPDF"""
    try:
        doc = fitz.open(pdf_path)
        text = ""
        for page in doc:
            text += page.get_text("text") + "\n"
        return text
    except Exception as e:
        logger.error(f"Failed to extract text from PDF: {str(e)}")
        return None

def extract_data_from_excel(file_path):
    """Extract data from Excel file using pandas"""
    try:
        df = pd.read_excel(file_path, sheet_name=None)  # Read all sheets
        return df
    except Exception as e:
        logger.error(f"Failed to extract data from Excel: {str(e)}")
        return None

def process_with_gemini(content, prompt_type="financial"):
    """Process content with Gemini AI"""
    try:
        model = genai.GenerativeModel("gemini-pro")
        
        prompts = {
            "financial": "Extract key financial data from this content. Return a JSON with these fields: total_revenue, total_expense, net_profit, assets, liabilities, equity. Format all numbers as floats.",
            "balance_sheet": "Analyze this balance sheet and extract key metrics. Return a JSON with total assets, total liabilities, and equity.",
            "income_statement": "Analyze this income statement and extract key metrics. Return a JSON with revenue, expenses, and net income."
        }
        
        prompt = prompts.get(prompt_type, prompts["financial"])
        response = model.generate_content(f"{prompt}\n\nContent:\n{content}")
        return response.text
    except Exception as e:
        logger.error(f"Failed to process with Gemini: {str(e)}")
        return None

def process_financial_document(document):
    """Process a financial document and extract data"""
    try:
        # Configure Gemini AI
        if not configure_genai():
            raise Exception("Failed to configure Gemini AI")
            
        file_path = document.file.path
        
        # Process based on file type
        if file_path.endswith('.pdf'):
            text = extract_text_from_pdf(file_path)
            if text:
                return process_with_gemini(text, prompt_type="financial")
        elif file_path.endswith(('.xlsx', '.xls')):
            df = extract_data_from_excel(file_path)
            if df is not None:
                # Convert all sheets to string representation
                content = "\n".join([f"Sheet: {name}\n{sheet.to_string()}" for name, sheet in df.items()])
                return process_with_gemini(content, prompt_type="financial")
        
        return None
    except Exception as e:
        logger.error(f"Failed to process financial document: {str(e)}")
        return None
