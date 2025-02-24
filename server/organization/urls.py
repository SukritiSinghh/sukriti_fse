from django.urls import path
from .views import (
    FileUploadView, 
    process_documents, 
    OrganizationViewSet,
    JoinOrganizationView,
    FinancialDataView
)

urlpatterns = [
    # Document related endpoints
    path('documents/upload/', FileUploadView.as_view(), name='file-upload'),
    path('documents/process/', process_documents, name='process-documents'),
    
    # Organization related endpoints
    path('organizations/', OrganizationViewSet.as_view(), name='organizations'),
    path('organizations/join/', JoinOrganizationView.as_view(), name='join-organization'),
    
    # Financial data related endpoints
    path('api/chargesheet/<int:company_id>/<int:year>/', FinancialDataView.as_view(), name='api_get_chargesheet'),
    path('api/balance-sheet/<int:company_id>/<int:year>/', FinancialDataView.as_view(), name='api_get_balance_sheet'),
    path('api/revenue-trend/<int:company_id>/', FinancialDataView.as_view(), name='api_get_revenue_trend'),
    path('api/anomalies/<int:company_id>/', FinancialDataView.as_view(), name='api_detect_anomalies'),
    path('api/forecast-revenue/<int:company_id>/', FinancialDataView.as_view(), name='api_forecast_revenue'),
]
