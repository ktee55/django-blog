from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.http import Http404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required, permission_required
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.models import User
# from django.urls import reverse_lazy
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Post, Comment, Category, Tag
from .forms import CommentForm

# for JSON data
from django.http.response import JsonResponse
from django.core import serializers

def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog/home.html', context)

class PostCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView): #-> post_form.html
  model = Post
  fields = ['title', 'content', 'featured_image', 'category', 'tags', 'draft']
  # success_url = reverse_lazy('blog-home')

  def form_valid(self, form):
    form.instance.author = self.request.user
    return super().form_valid(form)

  #ユーザーがスタッフの時にのみ許可
  def test_func(self):
    if self.request.user.is_staff:
        return True
    return False

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView): #-> post_form.html
  model = Post
  fields = ['title', 'content', 'featured_image', 'category', 'tags', 'draft']

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs) # はじめに継承元のメソッドを呼び出す
    context["edit"] = 1
    # context["photos"] = Photo.objects.all()
    # context["upload_form"] = UploadFileForm()
    # context["category_form"] = CategoryForm()
    # context["tag_form"] = TagForm()
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


def add_comment(request, post_id):

    #Still Need Validation!!,
    comment = Comment(
        comment=request.POST["comment"],
        author=request.user,
        post=Post.objects.get(pk=post_id)
    )
    comment.save()

    return redirect('post-detail', pk=post_id) 

class CommentCreateView(LoginRequiredMixin, UpdateView): 
    model = Comment
    fields = ['comment']

    def get_queryset(self):
      # post = get_object_or_404(Post, pk=self.kwargs.get('pk'))
      return Post.objects.filter(pk=self.kwargs.get('pk'))

    def form_valid(self, form):
      # post_id = self.kwargs['pk']
      # form.instance.post = Post.objects.get(pk=post_id)
      form.instance.author = self.request.user
      return super().form_valid(form)

class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView): 
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


@login_required
def comment_reject(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('post-detail', pk=comment.post.pk)


def paginate_queryset(request, queryset, count):

    paginator = Paginator(queryset, count)
    page = request.GET.get('page', 1) #1 for default page
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    return page_obj

def category(request, category_name):
  try:
    category = Category.objects.get(name=category_name)
  except Category.DoesNotExist:
    raise Http404("このカテゴリーは存在しません。")
  # category = get_object_or_404(Category, name=category_name)
  
  posts = category.posts.all()
  page_obj = paginate_queryset(request, posts, 2)

  context = {
    'category': category,
    'posts': page_obj.object_list,
    'page_obj': page_obj
  }
  return render(request, 'blog/post_list.html', context)

def tag(request, tag_name):
  try:
    tag = Tag.objects.get(name=tag_name)
  except Tag.DoesNotExist:
    raise Http404("このタグは存在しません。")

  tags = tag.posts.all()
  page_obj = paginate_queryset(request, tags, 2)

  context = {
    "tag": tag,
    'posts': page_obj.object_list,
    'page_obj': page_obj
  }
  return render(request, 'blog/post_list.html', context)


# Infinite scroll with javascript (failed because of csrf token issue)
def blog_api(request):

    # Get start and end point for posts to generate.
    # start = int(request.form.get("start") or 0)
    # end = int(request.form.get("end") or (start + 5))
    # posts = Post.objects.all()[0:5]
    
    posts = Post.objects.all()
    posts_serialized = serializers.serialize('json', posts)
    return JsonResponse(posts_serialized, safe=False) 


def json_posts(request):
    return render(request, 'blog/json_posts.html')