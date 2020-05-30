from django.urls import path
from .views import PostListView, PostDetailView, PostDeleteView, UserPostListView, TagPostListView, CategoryPostListView, CategoryCreateView, TagCreateView
#, PostCreateView, PostUpdateView, CommentUpdateView, CommentCreateView, CommentDeleteView 
from . import views

urlpatterns = [
    # path('', views.home, name='blog-home'),
    path('', PostListView.as_view(), name='blog-home'),
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    # path('post/create/', PostCreateView.as_view(), name='post-create'),
    path('post/create/', views.add_post, name='post-create'),
    # path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/update/', views.update_post, name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),

    path('post/<int:post_id>/comment/create', views.add_comment, name='comment-create'),
    path('comment/<int:comment_id>/update/', views.update_comment, name='comment-update'),
    path('comment/<int:comment_id>/delete/', views.delete_comment, name='comment-delete'),
    path('comment/<int:pk>/approve/', views.comment_approve, name='comment_approve'),
    path('category/create/', CategoryCreateView.as_view(), name='category-create'),
    path('tag/create/', TagCreateView.as_view(), name='tag-create'),
    path('category/<str:category_name>/', CategoryPostListView.as_view(), name='blog-category'),
    path('tag/<str:tag_name>/', TagPostListView.as_view(), name='blog-tag'),
    path('archives/', views.archives, name='post-archives'),

    path('about/', views.about, name='blog-about'),
    # path('version/', views.version, name='version'),

    # path('post/<int:post_id>/comment/create', CommentCreateView.as_view(), name='comment-create'),
    # path('comment/<int:pk>/update/', CommentUpdateView.as_view(), name='comment-update'),
    # path('comment/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment-delete'),
    # path('comment/<int:pk>/reject/', views.comment_reject, name='comment_reject'),

    # path('category/<str:category_name>/', views.category, name='blog-category'),
    # path('tag/<str:tag_name>/', views.tag, name='blog-tag'),
    #infinite scroll with Javascript
    # path('posts/api/', views.blog_api, name='blog_api'),
    # path('posts/', views.json_posts, name='json_posts'),
]