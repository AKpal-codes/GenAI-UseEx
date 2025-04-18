from django import forms

class DocumentUploadForm(forms.Form):
    file = forms.FileField(label='Select a file', help_text='max. 2.5 MB')