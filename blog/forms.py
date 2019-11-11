from django import forms
from .models import Comment, Post, URL #,Category, Tag
from django.forms.models import inlineformset_factory

class PostCreateForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['title', 'content', 'featured_image', 'category', 'tags', 'draft']

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
