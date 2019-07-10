from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.http import Http404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required, permission_required
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Post, Comment, Category, Tag
from photos.models import Photo
from .forms import CommentForm
from photos.forms import UploadFileForm


class PostListView(ListView):
  model = Post
  # template_name = 'blog/home.html' #default -> <app>/<model>_<viewtype>.html
  context_object_name = 'posts'
  ordering = ['-date_posted']
  paginate_by = 5

class UserPostListView(ListView):
  model = Post
  template_name = 'blog/post_list.html' 
  context_object_name = 'posts'
  # ordering = ['-date_posted']
  paginate_by = 5

  def get_queryset(self):
    user = get_object_or_404(User, username=self.kwargs.get('username'))
    return Post.objects.filter(author=user).order_by('-date_posted')

class PostDetailView(DetailView):  # -> post_detail.html
  model = Post
    # context_object_name = 'post'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs) 
    context["comment_form"] = CommentForm()
    return context

class PostCreateView(LoginRequiredMixin, CreateView): #-> post_form.html
  model = Post
  fields = ['title', 'content', 'category', 'tags']
  # success_url = reverse_lazy('blog-home')

  #追加データを渡す
  # def get_context_data(self, **kwargs):
  #   context = super().get_context_data(**kwargs) # はじめに継承元のメソッドを呼び出す
  #   context["photos"] = Photo.objects.all().order_by('-id')
  #   context["upload_form"] = UploadFileForm()
  #   return context

  def form_valid(self, form):
    form.instance.author = self.request.user
    return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView): #-> post_form.html
  model = Post
  fields = ['title', 'content', 'category', 'tags']

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs) # はじめに継承元のメソッドを呼び出す
    context["edit"] = 1
    context["photos"] = Photo.objects.all()
    context["upload_form"] = UploadFileForm()
    return context

  def form_valid(self, form):
    form.instance.author = self.request.user
    return super().form_valid(form)

  #ユーザーが投稿者の時にのみ許可
  def test_func(self):
    post = self.get_object()
    if self.request.user == post.author:
        return True
    return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView): #-> post_confirm_delete.html
  model = Post
  success_url = '/'

  #ユーザーが投稿者の時にのみ許可
  def test_func(self):
    post = self.get_object()
    if self.request.user == post.author:
        return True
    return False


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('post-detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/comment_form.html', {'form': form})

@login_required
def update_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.method == "POST":
      form = CommentForm(request.POST, instance=comment)
      if form.is_valid():
          comment = form.save(commit=False)
          if comment.author == request.user :
            comment.save()
            return redirect('post-detail', pk=comment.post.pk)
    else:
      form = CommentForm(instance=comment)
      context = {
        'form': form,
        'edit': 1,
        'post': comment.post,
      }

    return render(request, 'blog/comment_form.html', context)

@login_required
def delete_comment(request, comment_id):

    comment = Comment.objects.get(pk=comment_id)

    if request.method == "POST":
      post_id=comment.post.id
      # コメントの投稿者およびコメントされた投稿の投稿者に削除権(or Reject)を与える
      if comment.author == request.user or comment.post.author == request.user:
        comment.delete()
      return redirect('post-detail', pk=post_id) 

    else:
      context = {
        "comment": comment
      }
      return render(request, 'blog/comment_confirm_delete.html', context)


@login_required
# @permission_required('is_staff')
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    # if request.user.is_staff:
    if request.user == comment.post.author:
      comment.approve()
    return redirect('post-detail', pk=comment.post.pk)


class CategoryPostListView(ListView):
  model = Post
  template_name = 'blog/post_list.html' 
  context_object_name = 'posts'
  paginate_by = 2

  def get_queryset(self):
    category = get_object_or_404(Category, name=self.kwargs.get('category_name'))
    return category.posts.all()

class TagPostListView(ListView):
  model = Post
  template_name = 'blog/post_list.html' 
  context_object_name = 'posts'
  paginate_by = 2

  def get_queryset(self):
    tag = get_object_or_404(Tag, name=self.kwargs.get('tag_name'))
    return tag.posts.all()

def archives(request):
    month = request.GET.get('month')
    year = request.GET.get('year')
    posts = Post.objects.filter(date_posted__year=year, date_posted__month=month)
    context = {
        'posts': posts,
        'is_archives': 1,
        'month': month,
        'year': year
    }
    return render(request, 'blog/post_list.html', context)


def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})

# def version(request):
#     # import sys
#     # return HttpResponse(sys.version_info)
#     import pylint
#     return HttpResponse(pylint.__version__)

