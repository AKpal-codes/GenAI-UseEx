from django.shortcuts import render
from .forms import DocumentUploadForm
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
            context['uploaded'] = True
            context['file_name'] = uploaded_file.name
            context['file_path'] = file_path
    else:
        form = DocumentUploadForm()
    context['form'] = form
    return render(request, 'docparser/home.html', context)