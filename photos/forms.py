from django import forms
from .models import Photo

class UploadFileForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ["origin", ]
