from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

class Post(models.Model):
  title = models.CharField(max_length=100, verbose_name="タイトル")
  content = models.TextField(verbose_name="内容")
  # date_posted = models.DateTimeField(auto_now=True) #常に日付更新
  # date_posted = models.DateTimeField(auto_now_add=True) #作成時のみ更新。更新時日付更新されない。
  date_posted = models.DateTimeField(default=timezone.now)
  author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")

  class Meta:
    verbose_name_plural = '投稿'

  def __str__(self):
    return self.title

  def get_absolute_url(self):
      return reverse('post-detail', kwargs={'pk': self.pk})


