from django import forms

class DocumentUploadForm(forms.Form):
    file = forms.FileField(
        label='Select a Business Document',
        widget=forms.ClearableFileInput(attrs={
            'class': 'form-control',
            'placeholder': 'Choose a file'
        })
    )