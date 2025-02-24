from django.urls import path
from .views import FileUploadView, ProcessDocumentView

urlpatterns = [
    path('upload/', FileUploadView.as_view(), name='file-upload'),
    path('save/', FileUploadView.as_view(), name='save-document'),
    path('process/<int:document_id>/', ProcessDocumentView.as_view(), name='process-document'),
]
