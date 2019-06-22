from django import forms
from .models import Comment, Photo

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['comment']

class UploadFileForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ["origin", ]