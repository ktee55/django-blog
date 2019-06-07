from django.db import models
from django.utils import timezone

class Post(models.Model):
  title = models.CharField(max_length=100)
  content = models.TextField()
  # date_posted = models.DateTimeField(auto_now=True) #常に日付更新
  # date_posted = models.DateTimeField(auto_now_add=True) #作成時のみ更新。更新時日付更新されない。
  date_posted = models.DateTimeField(default=timezone.now)
