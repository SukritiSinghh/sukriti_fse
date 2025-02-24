from django.urls import path
from .views import FileUploadView, process_documents

urlpatterns = [
    path('upload/', FileUploadView.as_view(), name='file-upload'),
    path('process/', process_documents, name='process-documents'),
]
