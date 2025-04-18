from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from .forms import DocumentUploadForm
from .utils.extractor import extract_text
from .utils.genai import analyze_document_with_genai
import os

# Create your views here.
def home(request):
    context = {}
    if request.method == 'POST' and 'file' in request.FILES:
        form = DocumentUploadForm(request.POST, request.FILES)
        if form.is_valid():            
            uploaded_file = request.FILES['file']

            fs = FileSystemStorage()
            filename = fs.save(uploaded_file.name, uploaded_file)
            file_path = fs.path(filename)

            try:
                extracted_text = extract_text(file_path)
                if not extracted_text.strip():
                    context['error'] = "The extracted text is empty. Please try a different file."
                else:
                    genai_output = analyze_document_with_genai(extracted_text)
                    context['text'] = extracted_text
                    context['genai_output'] = genai_output

                    if os.path.exists(file_path):
                        os.remove(file_path)
            except Exception as e:
                context['error'] = str(e)

            context['uploaded'] = True
            context['file_name'] = uploaded_file.name
            
    else:
        form = DocumentUploadForm()
    context['form'] = form
    return render(request, 'docparser/home.html', context)