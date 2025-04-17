from django import forms

class DocumentUploadForm(forms.Form):
    """
    Form for uploading documents.
    """
    file = forms.FileField(label='Select a file', help_text='max. 42 megabytes')