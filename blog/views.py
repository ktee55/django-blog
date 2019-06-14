from django.shortcuts import render, redirect, HttpResponse
from django.http import Http404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Comment, Category, Tag
from django.urls import reverse_lazy

# posts = [
#     {
#         'author': 'CoreyMS',
#         'title': 'Blog Post 1',
#         'content': 'First post content',
#         'date_posted': 'August 27, 2018'
#     },
#     {
#         'author': 'Jane Doe',
#         'title': 'Blog Post 2',
#         'content': 'Second post content',
#         'date_posted': 'August 28, 2018'
#     }
# ]


def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog/home.html', context)

class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html' #default -> <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']

class PostDetailView(DetailView):  # -> post_detail.html
    model = Post
    # context_object_name = 'post'

class PostCreateView(LoginRequiredMixin, CreateView): #-> post_form.html
    model = Post
    fields = ['title', 'content', 'category', 'tags']
    # success_url = reverse_lazy('blog-home')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView): #-> post_form.html
    model = Post
    fields = ['title', 'content', 'category', 'tags']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView): #-> post_confirm_delete.html
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def add_comment(request, post_id):

    #Still Need Validation!!,
    comment = Comment(
        comment=request.POST["comment"],
        author=request.user,
        post=Post.objects.get(pk=post_id)
    )
    comment.save()

    return redirect('post-detail', pk=post_id) 

class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView): #-> post_form.html
    model = Comment
    fields = ['comment']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        comment = self.get_object()
        if self.request.user == comment.author:
            return True
        return False

class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView): 
    model = Comment
    # Wanna to go back to the post that comment attached
    success_url = '/'

    def test_func(self):
        comment = self.get_object()
        if self.request.user == comment.author:
            return True
        return False

# def delete_comment(request, comment_id):

#     #Need Confirmation
#     comment = Comment.objects.get(pk=comment_id)
#     post_id=comment.post.id
#     comment.delete()

#     return redirect('post-detail', pk=post_id) 


def category(request, category_id):
  try:
    category = Category.objects.get(pk=category_id)
  except Category.DoesNotExist:
    raise Http404("このカテゴリーは存在しません。")
  context = {
    "category": category
  }
  return render(request, 'blog/category.html', context)


def tag(request, tag_id):
  try:
    tag = Tag.objects.get(pk=tag_id)
  except Tag.DoesNotExist:
    raise Http404("このタグは存在しません。")
  context = {
    "tag": tag
  }
  return render(request, 'blog/tag.html', context)

def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})

# def version(request):
#     # import sys
#     # return HttpResponse(sys.version_info)
#     import pylint
#     return HttpResponse(pylint.__version__)
