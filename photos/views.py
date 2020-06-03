from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required, permission_required
from django.urls import reverse_lazy
from django.db.models import Q

from .models import Photo, Category, Tag
# from .forms import UploadFileForm
from .forms import UploadMultipleFormSet
from blog.boost import DynamicRedirectMixin

class PhotoListView(ListView):
    model = Photo
    context_object_name = 'photos'
    ordering = ['-id']
    paginate_by = 6

    def get_queryset(self):
      if self.request.user.is_authenticated:
        user = self.request.user
        return Photo.objects.filter( Q(private=False) | Q(author=user) ).order_by('-id')
      else:
        return Photo.objects.filter(private=False).order_by('-id')


class PhotoDetailView(UserPassesTestMixin, DetailView):
  model = Photo

  def get_context_data(self, **kwargs):
    photo = self.get_object()
    context = super().get_context_data(**kwargs) 

    try:
      context["next"] = photo.get_next_by_date_posted(private=False)
    except:
      context["next"] = None

    try:
      context["previous"] = photo.get_previous_by_date_posted(private=False)
    except:
      context["previous"] = None

    return context

  #写真が非公開になっていないか、非公開になっててもユーザーが投稿者本人の時表示する。
  def test_func(self):
    photo = self.get_object()
    if not photo.private or self.request.user == photo.author:
        return True
    return False

# class PhotoCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView): 
#   model = Photo
#   fields = ['origin', 'category', 'tags', 'private']
#   success_url = reverse_lazy('photo-list')

#   def form_valid(self, form):
#     form.instance.author = self.request.user
#     return super().form_valid(form)

#   #ユーザーがスタッフの時にのみ許可
#   def test_func(self):
#     if self.request.user.is_staff:
#         return True
#     return False

@permission_required('is_staff')
def create_photo(request):
    if request.method == "POST":
        # formset = UploadMultipleFormSet(request.POST or None, files=request.FILES or None, queryset=Photo.objects.none())
        formset = UploadMultipleFormSet(request.POST, files=request.FILES)
        if formset.is_valid():
            photos = formset.save(commit=False)
            for photo in photos:
              photo.author = request.user
              photo.save()
            return redirect('photo-list')
    else:
        formset = UploadMultipleFormSet(queryset=Photo.objects.none())
    return render(request, 'photos/photo_form.html', {'form': formset})

# def create_photo(request):
#     if request.method == "POST":
#         form = UploadFileForm(request.POST, request.FILES)
#         if form.is_valid():
#             photo = form.save()
#             next = request.POST.get('next', '/')
#             photo.save()
#             return redirect(next)
#     else:
#         form = UploadFileForm()
#     return render(request, 'blog/photo_form.html', {'form': form})

class PhotoUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView): 
  model = Photo
  fields = ['category', 'tags', 'private']

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs) # はじめに継承元のメソッドを呼び出す
    context["edit"] = 1
    return context

  def form_valid(self, form):
    form.instance.author = self.request.user
    return super().form_valid(form)

  #ユーザーが投稿者の時にのみ許可
  def test_func(self):
    photo = self.get_object()
    if self.request.user == photo.author:
        return True
    return False


class PhotoDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView): 
  model = Photo
  success_url = reverse_lazy('photo-list')

  #ユーザーが投稿者の時にのみ許可
  def test_func(self):
    photo = self.get_object()
    if self.request.user == photo.author:
        return True
    return False


class CategoryCreateView(LoginRequiredMixin, UserPassesTestMixin, DynamicRedirectMixin, CreateView): 
  model=Category
  fields = ['name']
  # success_url = reverse_lazy('category-create')

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs) 
    context["photo_categories"] = Category.objects.all()
    return context

  #ユーザーがスタッフの時にのみ許可
  def test_func(self):
    if self.request.user.is_staff:
        return True
    return False


class TagCreateView(LoginRequiredMixin, UserPassesTestMixin, DynamicRedirectMixin, CreateView): 
  model=Tag
  fields = ['name']
  # success_url = reverse_lazy('category-create')

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs) 
    context["photo_tags"] = Tag.objects.all()
    return context

  #ユーザーがスタッフの時にのみ許可
  def test_func(self):
    if self.request.user.is_staff:
        return True
    return False