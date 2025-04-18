from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from .forms import DocumentUploadForm
from .utils.extractor import extract_text
from .utils.genai import analyze_document_with_genai
from .utils.doc_builder import save_response_to_word
import os

# Create your views here.
def home(request):
    context = {}
    if request.method == 'POST' and 'file' in request.FILES:
        form = DocumentUploadForm(request.POST, request.FILES)
        if form.is_valid():            
            uploaded_file = request.FILES['file']

            for file in os.listdir("media/"):
                if file.endswith(".docx"):
                    os.remove(os.path.join("media/", file))

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

                    try:
                        download_path = save_response_to_word(genai_output)
                        context['download_link'] = '/' + download_path  # for <a href> in template                        
                    except Exception as e:
                        context['download_error'] = f"Could not generate Word file: {str(e)}"



            except Exception as e:
                context['error'] = str(e)

            context['uploaded'] = True
            context['file_name'] = uploaded_file.name
            
    else:
        form = DocumentUploadForm()
    context['form'] = form
    return render(request, 'docparser/home.html', context)