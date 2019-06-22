from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from imagekit.models import ImageSpecField, ProcessedImageField
from imagekit.processors import ResizeToFill

class Tag(models.Model):
  name = models.CharField(max_length=100, verbose_name="タグ")

  class Meta:
    verbose_name_plural = 'タグ'

  def __str__(self):
    return self.name

class Category(models.Model):
  name = models.CharField(max_length=100, verbose_name="カテゴリー")

  class Meta:
    verbose_name_plural = 'カテゴリー'

  def __str__(self):
    return self.name


class Post(models.Model):
  title = models.CharField(max_length=100, verbose_name="タイトル")
  content = models.TextField(verbose_name="内容")
  # date_posted = models.DateTimeField(auto_now=True) #常に日付更新
  # date_posted = models.DateTimeField(auto_now_add=True) #作成時のみ更新。更新時日付更新されない。
  date_posted = models.DateTimeField(default=timezone.now)

  author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
  category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="posts", null=True, blank=True)
  tags = models.ManyToManyField(Tag, blank=True, related_name="posts")

  class Meta:
    verbose_name_plural = "投稿"

  def __str__(self):
    return self.title

  def get_absolute_url(self):
      return reverse('post-detail', kwargs={'pk': self.pk})

  def approved_comments(self):
    return self.comments.filter(approved_comment=True)


class Comment(models.Model):
  comment = models.TextField(verbose_name="コメント")
  date_posted = models.DateTimeField(default=timezone.now)
  author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
  post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
  approved_comment = models.BooleanField(default=False)

  class Meta:
    verbose_name_plural = "コメント"

  def __str__(self):
    return f"{self.comment}"

  def get_absolute_url(self):
      #going back to the post that comment attached
      return reverse('post-detail', kwargs={'pk': self.post.pk})

  def approve(self):
    self.approved_comment = True
    self.save()


class Photo(models.Model):

    origin = models.ImageField(upload_to="photos/%y/%m/%d/")

    large = ImageSpecField(source="origin",
                         processors=[ResizeToFill(1280, 1024)],
                         format='JPEG'
                         )

    medium = ImageSpecField(source='origin',
                        processors=[ResizeToFill(600, 400)],
                        format="JPEG",
                        options={'quality': 75}
                        )

    small = ImageSpecField(source='origin',
                            processors=[ResizeToFill(250,250)],
                            format="JPEG",
                            options={'quality': 60}
                            )

    thumbnail= ImageSpecField(source='origin',
                            processors=[ResizeToFill(75,75)],
                            format="JPEG",
                            options={'quality': 50}
                            )