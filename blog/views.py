from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.http import Http404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required, permission_required
from django.views.decorators.http import condition
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.core.mail import send_mail

from .models import Post, Comment, Category, Tag
# from photos.models import Photo
from .forms import CommentForm, PostCreateForm, URLFormset
# from photos.forms import UploadFileForm
from .boost import DynamicRedirectMixin


class PostListView(ListView):
  model = Post
  # template_name = 'blog/home.html' #default -> <app>/<model>_<viewtype>.html
  context_object_name = 'posts'
  # ordering = ['-date_posted']
  paginate_by = 5

  def get_queryset(self):
      if self.request.user.is_authenticated:
        user = self.request.user
        return Post.objects.filter( Q(draft=False) | Q(author=user) ).order_by('-date_posted')
      else:
        return Post.objects.filter(draft=False).order_by('-date_posted')

class UserPostListView(ListView):
  model = Post
  template_name = 'blog/post_list.html' 
  context_object_name = 'posts'
  paginate_by = 5

  def get_queryset(self):
    user = get_object_or_404(User, username=self.kwargs.get('username'))
    return Post.objects.filter(author=user).order_by('-date_posted')

class PostDetailView(UserPassesTestMixin, DetailView):  # -> post_detail.html
  model = Post
    # context_object_name = 'post'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs) 
    context["comment_form"] = CommentForm()
    post = self.get_object()

    try:
      context["next"] = post.get_next_by_date_posted(draft=False)
    except:
      context["next"] = None

    try:
      context["previous"] = post.get_previous_by_date_posted(draft=False)
    except:
      context["previous"] = None

    return context

  #投稿が下書きになっていないか、下書きになっててもユーザーが投稿者本人の時表示する。
  def test_func(self):
    post = self.get_object()
    if not post.draft or self.request.user == post.author:
        return True
    return False

@permission_required('is_staff')
def add_post(request):
    form = PostCreateForm(request.POST or None, files=request.FILES or None)
    context = {'form': form}
    if request.method == 'POST' and form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        formset = URLFormset(request.POST, instance=post)  # 今回はファイルなのでrequest.FILESが必要
        if formset.is_valid():
            post.save()
            formset.save()
            return redirect('blog-home')
        # エラーメッセージつきのformsetをテンプレートへ渡すため、contextに格納
        else:
            context['formset'] = formset

    # GETのとき
    else:
        # 空のformsetをテンプレートへ渡す
        context['formset'] = URLFormset()

    return render(request, 'blog/post_form.html', context)

@login_required
def update_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if not post.author == request.user:
      return redirect('blog-home')
    form = PostCreateForm(request.POST or None, files=request.FILES or None, instance=post)
    formset = URLFormset(request.POST or None, instance=post)
    if request.method == 'POST' and form.is_valid() and formset.is_valid() and request.user == post.author:
        form.save()
        formset.save()
        # 編集ページを再度表示
        return redirect('post-detail', pk=pk)

    context = {
        'post': post,
        'form': form,
        'formset': formset,
        'edit': 1,
    }

    return render(request, 'blog/post_form.html', context)

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
            if post.author == request.user:
              comment.approved_comment = True
            comment.save()
            send_mail(
              f'{request.user.username} left a comment on {post.title}',
              f'{comment.comment}',
              'uncleko496@gmail.com',
              ['uncleko496@gmail.com', post.author.email],
              fail_silently=False,
            ) 
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
          if not comment.post.author == request.user:
            comment.approved_comment = False
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
  paginate_by = 5

  def get_queryset(self):
    category = get_object_or_404(Category, name=self.kwargs.get('category_name'))
    return category.posts.filter(draft=False).order_by('-date_posted')

class TagPostListView(ListView):
  model = Post
  template_name = 'blog/post_list.html' 
  context_object_name = 'posts'
  paginate_by = 5

  def get_queryset(self):
    tag = get_object_or_404(Tag, name=self.kwargs.get('tag_name'))
    return tag.posts.filter(draft=False).order_by('-date_posted')

def archives(request):
    month = request.GET.get('month')
    year = request.GET.get('year')
    posts = Post.objects.filter(date_posted__year=year, date_posted__month=month, draft=False).order_by('-date_posted')
    context = {
        'posts': posts,
        'is_archives': 1,
        'month': month,
        'year': year
    }
    return render(request, 'blog/post_list.html', context)


class CategoryCreateView(LoginRequiredMixin, UserPassesTestMixin, DynamicRedirectMixin, CreateView): 
  model=Category
  fields = ['name']
  success_url = reverse_lazy('category-create')

  # def get_context_data(self, **kwargs):
  #   context = super().get_context_data(**kwargs) 
  #   context["post_categories"] = Category.objects.all() ==> context_processors.pyで既に渡されてる
  #   return context

  #ユーザーがスタッフの時にのみ許可
  def test_func(self):
    if self.request.user.is_staff:
        return True
    return False


class TagCreateView(LoginRequiredMixin, UserPassesTestMixin, DynamicRedirectMixin, CreateView): 
  model=Tag
  fields = ['name']
  success_url = reverse_lazy('tag-create')

  # def get_context_data(self, **kwargs):
  #   context = super().get_context_data(**kwargs) 
  #   context["post_tags"] = Tag.objects.all() ==> context_processors.pyで既に渡されてる
  #   return context

  #ユーザーがスタッフの時にのみ許可
  def test_func(self):
    if self.request.user.is_staff:
        return True
    return False




def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})

# def version(request):
#     # import sys
#     # return HttpResponse(sys.version_info)
#     import pylint
#     return HttpResponse(pylint.__version__)

