from django.urls import path
from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, CommentUpdateView, CommentDeleteView
from . import views

urlpatterns = [
    # path('', views.home, name='blog-home'),
    path('', PostListView.as_view(), name='blog-home'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/create/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),

    path('post/<int:post_id>/comment/create', views.add_comment, name='comment-create'),
    path('comment/<int:pk>/update/', CommentUpdateView.as_view(), name='comment-update'),
    path('comment/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment-delete'),
    # path('comment/<int:comment_id>/delete/', views.delete_comment, name='comment-delete'),

    path('category/<int:category_id>/', views.category, name='blog-category'),
    path('tag/<int:tag_id>/', views.tag, name='blog-tag'),

    path('about/', views.about, name='blog-about'),
    # path('version/', views.version, name='version'),
]