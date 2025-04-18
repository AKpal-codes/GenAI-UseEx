from django.shortcuts import render
from .forms import DocumentUploadForm
from .utils.extractor import extract_text
import os
# Create your views here.
def home(request):
    context = {}
    if request.method == 'POST':
        form = DocumentUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # Handle the uploaded file
            uploaded_file = request.FILES['file']
            file_path = os.path.join('media', uploaded_file.name)
            with open(file_path, 'wb+') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)

            try:
                extracted_text = extract_text(file_path)
                context['text'] = extracted_text
            except Exception as e:
                context['error'] = str(e)

            context['uploaded'] = True
            context['file_name'] = uploaded_file.name
            
    else:
        form = DocumentUploadForm()
    context['form'] = form
    return render(request, 'docparser/home.html', context)