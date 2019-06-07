from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Post(models.Model):
  title = models.CharField(max_length=100)
  content = models.TextField()
  # date_posted = models.DateTimeField(auto_now=True) #常に日付更新
  # date_posted = models.DateTimeField(auto_now_add=True) #作成時のみ更新。更新時日付更新されない。
  date_posted = models.DateTimeField(default=timezone.now)
  author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")

  def __str__(self):
    return self.title

