from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from .forms import DocumentUploadForm
from .utils.extractor import extract_text
from .utils.genai import analyze_document_with_genai
from .utils.doc_builder import save_response_to_word
import os
import json
import re

def clean_genai_response(response_text):
    # Remove triple backticks and optional `json` label
    pattern = r"```(?:json)?\n(.*?)\n```"
    match = re.search(pattern, response_text, re.DOTALL)

    if match:
        return match.group(1).strip()
    
    # If no backticks found, assume raw JSON
    return response_text.strip()

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
                    genai_response = clean_genai_response(genai_output)
                    parsed_response = json.loads(genai_response)
                    modules = parsed_response.get("modules", [])
                    use_cases = parsed_response.get("use_cases", [])
                    stakeholders = parsed_response.get("stakeholders", [])
                    risks = parsed_response.get("risks", [])
                    timeline_priority = parsed_response.get("timeline_priority", [])

                    context.update({
                        'text': extracted_text,
                        'genai_output': genai_response,
                        'modules': modules,
                        'use_cases': use_cases,
                        'stakeholders': stakeholders,
                        'risks': risks,
                        'timeline_priority': timeline_priority
                    })

                    if os.path.exists(file_path):
                        os.remove(file_path)

                    try:
                        download_path = save_response_to_word(genai_response)
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