from django.urls import path, include
from .views import PhotoListView, PhotoCreateView, PhotoDeleteView

urlpatterns = [
    path('', PhotoListView.as_view(), name='photo-list'),
    path('create/', PhotoCreateView.as_view(), name='photo-create'),
    # path('photo/create/', views.create_photo, name='photo-create'),
    path('<int:pk>/delete', PhotoDeleteView.as_view(), name='photo-delete'),
]