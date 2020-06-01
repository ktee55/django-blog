from django.urls import path, include
from .views import PhotoListView, PhotoDetailView, create_photo, PhotoUpdateView, PhotoDeleteView, CategoryCreateView, TagCreateView

urlpatterns = [
    path('', PhotoListView.as_view(), name='photo-list'),
    path('<int:pk>/', PhotoDetailView.as_view(), name='photo-detail'),
    path('create/', create_photo, name='photo-create'),
    # path('create/', PhotoCreateView.as_view(), name='photo-create'),
    path('<int:pk>/update/', PhotoUpdateView.as_view(), name='photo-update'),
    path('<int:pk>/delete', PhotoDeleteView.as_view(), name='photo-delete'),
    path('category/create/', CategoryCreateView.as_view(), name='photo-category-create'),
    path('tag/create/', TagCreateView.as_view(), name='photo-tag-create'),
]