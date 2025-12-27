import os
from django.shortcuts import render
from django.http import HttpResponse
from pdf2docx import Converter
import tempfile


def home(request):
    if request.method == "POST":
        uploaded_file = request.FILES['pdf_file']
        name_only, _ = os.path.splitext(uploaded_file.name)

        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
            for chunk in uploaded_file.chunks():
                temp_pdf.write(chunk)
            temp_pdf_path = temp_pdf.name

        docx_file_path = temp_pdf_path.replace(".pdf", ".docx")

        try:
            cv = Converter(temp_pdf_path)
            cv.convert(docx_file_path, start=0, end=None)
            cv.close()

            with open(docx_file_path, 'rb') as f:
                docx_data = f.read()

            response = HttpResponse(
                docx_data,
                content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )
            response["Content-Disposition"] = f'attachment; filename="{name_only}.docx"'

            return response

        finally:
            if os.path.exists(temp_pdf_path):
                os.remove(temp_pdf_path)
            if os.path.exists(docx_file_path):
                os.remove(docx_file_path)

    return render(request, "index.html")
