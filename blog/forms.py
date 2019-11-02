from django import forms
from .models import Comment #, Post, Category, Tag
# from django.forms.models import inlineformset_factory

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['comment']

# class CategoryForm(forms.ModelForm):

#     class Meta:
#         model = Category
#         fields = ['name']

# class TagForm(forms.ModelForm):

#     class Meta:
#         model = Tag
#         fields = ['name']

# PostFormset = inlineformset_factory(
#     Category,
#     Post
# )