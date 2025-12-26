from django.shortcuts import render
import fitz
from django.http import HttpResponse
from docx import Document
import os

def home(request):
    if request.method == "POST":
        uploaded_file = request.FILES['pdf_file']
        name_only, extension = os.path.splitext(uploaded_file.name)
        new_filename = f"{name_only}.docx"

        pdf_bytes = uploaded_file.read()
        pdf_doc = fitz.open(stream=pdf_bytes, filetype="pdf")

        word_doc = Document()
        for page_num, page in enumerate(pdf_doc, start=1):
            text = page.get_text()
            word_doc.add_paragraph(text)

        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        )
        response['Content-Disposition'] = f'attachment; filename="{new_filename}"'
        word_doc.save(response)
        return response

    return render(request, 'index.html')
