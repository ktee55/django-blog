from django.contrib import admin
from django.urls import path, include
from users import views as user_views
# from users.views import register

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', user_views.register, name='register'),
    # path('register/', register, name='register'),
    path('', include('blog.urls')),
]
