from django.urls import path
from .views import (
    FileUploadView, 
    process_documents, 
    OrganizationViewSet,
    JoinOrganizationView,
    FinancialDataView,
    api_get_chargesheet,
    api_get_balance_sheet,
    api_get_revenue_trend,
    api_detect_anomalies,
    api_forecast_revenue
)

urlpatterns = [
    # Document related endpoints
    path('documents/upload/', FileUploadView.as_view(), name='upload-document'),
    path('documents/process/', process_documents, name='process-documents'),
    
    # Organization related endpoints
    path('organizations/', OrganizationViewSet.as_view(), name='organizations'),
    path('organizations/join/', JoinOrganizationView.as_view(), name='join-organization'),
    
    # Financial data related endpoints
    path('financial-data/', FinancialDataView.as_view(), name='financial_data'),
    path('chargesheet/', api_get_chargesheet, name='api_get_chargesheet'),
    path('balance-sheet/', api_get_balance_sheet, name='api_get_balance_sheet'),
    path('revenue-trend/', api_get_revenue_trend, name='api_get_revenue_trend'),
    path('anomalies/', api_detect_anomalies, name='api_detect_anomalies'),
    path('forecast-revenue/', api_forecast_revenue, name='api_forecast_revenue'),
]
