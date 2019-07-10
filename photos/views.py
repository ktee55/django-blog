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
    paginate_by = 10

class PhotoCreateView(LoginRequiredMixin, CreateView): 
  model = Photo
  fields = ['origin']
  success_url = reverse_lazy('photo-list')

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

class PhotoDeleteView(LoginRequiredMixin, DeleteView): 
  model = Photo
  success_url = reverse_lazy('photo-list')
