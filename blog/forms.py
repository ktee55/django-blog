from django import forms
from .models import Comment, Post, URL,Category, Tag
from django.forms.models import inlineformset_factory
# from django.forms.widgets import ClearableFileInput
from os import path

# #既に保存してあるFileの現在パスをファイル名だけにする
# #UpdateでOK, Createでエラー
# class CustomClearableFileInput(ClearableFileInput):
#     def get_context(self, name, value, attrs):
#         value.name = path.basename(value.name)
#         context = super().get_context(name, value, attrs)       
#         return context

class PostCreateForm(forms.ModelForm):
    title = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'textinput textInput form-control'
        })
    )
    # featured_image = forms.ImageField(
    #     # widget=CustomClearableFileInput
    # )
    content = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'textarea form-control'
        })
    )
    category = forms.ModelChoiceField(
        widget=forms.Select(attrs={
            'class': 'select form-control'
        }),
        queryset=Category.objects.all(),
        required=False
    )
    tags = forms.ModelMultipleChoiceField(
        widget=forms.SelectMultiple(attrs={
            'class': 'selectmultiple form-control'
        }),
        queryset=Tag.objects.all(),
        required=False
    )
    draft = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={
            'class': 'checkboxinput form-check-input'
        }),
        required=False
    )
    

    class Meta:
        model = Post
        fields = ['title', 'featured_image', 'content', 'category', 'tags', 'draft']

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['comment', 'url']

URLFormset = inlineformset_factory(
    Post,
    URL,
    fields='__all__',
    extra=10,
    max_num=10,
    # can_delete=False
)

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
