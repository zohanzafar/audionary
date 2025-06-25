from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from django.core.files.storage import default_storage
from .utils.pdf_parser import extract_text_from_pdf, chunk_text
from .utils.summary_agent import run_summary_agent
from .utils.tts_converter import generate_audio
from django.shortcuts import render
from rest_framework import status


def frontend_view(request):
    return render(request, 'index.html')


class UploadPDFView(APIView):
    parser_classes = [MultiPartParser]
    MAX_FILE_SIZE_MB = 10  # ⬅️ 10 MB limit

    def post(self, request):
        try:
            pdf = request.data.get("file")

            # ✅ Validate file existence
            if not pdf:
                return Response({"error": "No file uploaded."}, status=status.HTTP_400_BAD_REQUEST)

            # ✅ Validate file type
            if not pdf.name.endswith('.pdf') or pdf.content_type != 'application/pdf':
                return Response({"error": "Only PDF files are allowed."}, status=status.HTTP_400_BAD_REQUEST)

            # ✅ Validate file size (10 MB limit)
            max_size_bytes = self.MAX_FILE_SIZE_MB * 1024 * 1024
            if pdf.size > max_size_bytes:
                return Response(
                    {"error": f"File exceeds the maximum size of {self.MAX_FILE_SIZE_MB} MB."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # ✅ Save file to media/uploads
            path = default_storage.save(f"uploads/{pdf.name}", pdf)

            # ✅ Extract text
            full_path = default_storage.path(path)
            text = extract_text_from_pdf(full_path)
            if not text.strip():
                return Response({"error": "The PDF appears to be empty or unreadable."}, status=status.HTTP_400_BAD_REQUEST)

            # ✅ Chunking
            chunks = chunk_text(text)

            # ✅ Run summary + narration
            narration = run_summary_agent(chunks)
            if not narration:
                return Response({"error": "Failed to generate narration."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            # ✅ Generate audio
            audio_file = generate_audio(narration)

            return Response({
                "message": "PDF processed and audio generated successfully.",
                "narration_preview": narration[:],
                "audio_url": request.build_absolute_uri(f"/media/audio/{audio_file}")
            })

        except Exception as e:
            print("UploadPDFView error:", str(e))  # Log for debugging
            return Response({
                "error": "Something went wrong while processing the PDF. Please try again later."
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DownloadAudioView(APIView):
    def get(self, request, file_name):
        path = default_storage.path(f'audio/{file_name}')
        with open(path, 'rb') as f:
            return Response(f.read(), content_type='audio/mpeg')
