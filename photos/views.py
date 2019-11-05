from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy

from .models import Photo
from .forms import UploadFileForm

class PhotoListView(ListView):
    model = Photo
    context_object_name = 'photos'
    ordering = ['-id']
    paginate_by = 6


class PhotoDetailView(UserPassesTestMixin, DetailView):
  model = Photo

  def get_context_data(self, **kwargs):
    photo = self.get_object()
    context = super().get_context_data(**kwargs) 
    context["next"] = photo.get_next_by_date_posted
    context["previous"] = photo.get_previous_by_date_posted
    return context

  #写真が非公開になっていないか、非公開になっててもユーザーが投稿者本人の時表示する。
  def test_func(self):
    photo = self.get_object()
    if not photo.private or self.request.user == photo.author:
        return True
    return False

class PhotoCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView): 
  model = Photo
  fields = ['origin', 'private', 'category', 'tags']
  success_url = reverse_lazy('photo-list')

  def form_valid(self, form):
    form.instance.author = self.request.user
    return super().form_valid(form)

  #ユーザーがスタッフの時にのみ許可
  def test_func(self):
    if self.request.user.is_staff:
        return True
    return False

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
  fields = ['private', 'category', 'tags']

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