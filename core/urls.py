from django.urls import path
from .views import frontend_view, UploadPDFView, DownloadAudioView

urlpatterns = [
    path('upload-pdf/', UploadPDFView.as_view()),
    path('audio/<str:file_name>/', DownloadAudioView.as_view()),
]
