from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse
from .models import Document
from .serializers import DocumentSerializer
from .analytics import process_csv
from .pdf_utils import generate_pdf_report
import os
from rest_framework import permissions
from rest_framework.generics import CreateAPIView
from django.contrib.auth.models import User
from .serializers import DocumentSerializer, UserSerializer

class FileUploadView(APIView):
    def post(self, request, *args, **kwargs):
        file_serializer = DocumentSerializer(data=request.data)
        if file_serializer.is_valid():
            document = file_serializer.save()
            
            # Process the file
            analysis_result = process_csv(document.file.path)
            
            if "error" in analysis_result:
                # cleanup if error (optional, but good practice)
                # os.remove(document.file.path)
                # document.delete()
                return Response(analysis_result, status=status.HTTP_400_BAD_REQUEST)
            
            # Save summary to DB
            document.summary = analysis_result
            document.save()

            # Enforce last 5 datasets limit
            # Get all documents ordered by uploaded_at desc
            docs = Document.objects.order_by('-uploaded_at')
            if docs.count() > 5:
                # delete the older ones
                for doc in docs[5:]:
                    if doc.file:
                        if os.path.isfile(doc.file.path):
                             os.remove(doc.file.path)
                    doc.delete()

            return Response({
                "message": "File uploaded and processed successfully",
                "document_id": document.id,
                "analysis": analysis_result
            }, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class HistoryView(APIView):
    def get(self, request, *args, **kwargs):
        # Get last 5 documents
        documents = Document.objects.order_by('-uploaded_at')[:5]
        serializer = DocumentSerializer(documents, many=True)
        return Response(serializer.data)

class DocumentDetailView(APIView):
    """
    Retrieve details (including analysis) of a specific document
    """
    def get(self, request, pk, *args, **kwargs):
        try:
            document = Document.objects.get(pk=pk)
            serializer = DocumentSerializer(document)
            return Response(serializer.data)
        except Document.DoesNotExist:
             return Response({"error": "Document not found"}, status=status.HTTP_404_NOT_FOUND)

class PDFReportView(APIView):
    def get(self, request, pk, *args, **kwargs):
        try:
            document = Document.objects.get(pk=pk)
            if not document.summary:
                return Response({"error": "No analysis available for this document"}, status=status.HTTP_400_BAD_REQUEST)
            
            pdf_buffer = generate_pdf_report(document.summary)
            
            response = HttpResponse(pdf_buffer, content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="report_{pk}.pdf"'
            return response
        except Document.DoesNotExist:
             return Response({"error": "Document not found"}, status=status.HTTP_404_NOT_FOUND)

class RegisterView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

