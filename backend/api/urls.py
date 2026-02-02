from django.urls import path
from .views import FileUploadView, HistoryView, DocumentDetailView, PDFReportView

urlpatterns = [
    path('upload/', FileUploadView.as_view(), name='file-upload'),
    path('history/', HistoryView.as_view(), name='history'),
    path('history/<int:pk>/', DocumentDetailView.as_view(), name='document-detail'),
    path('history/<int:pk>/pdf/', PDFReportView.as_view(), name='pdf-report'),
]
