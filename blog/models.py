from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

from imagekit.models import ImageSpecField, ProcessedImageField
from imagekit.processors import ResizeToFill, ResizeToFit

class Tag(models.Model):
  name = models.CharField(max_length=100, verbose_name="タグ")

  class Meta:
    verbose_name_plural = 'タグ'

  def __str__(self):
    return self.name

  def published_posts(self):
    return self.posts.filter(draft=False)

class Category(models.Model):
  name = models.CharField(max_length=100, verbose_name="カテゴリー")

  class Meta:
    verbose_name_plural = 'カテゴリー'

  def __str__(self):
    return self.name

  def published_posts(self):
    return self.posts.filter(draft=False)


class Post(models.Model):
  title = models.CharField(max_length=100, verbose_name="タイトル")
  featured_image = models.ImageField(blank=True, upload_to='featured_image/%y/%m/', verbose_name="メイン画像(option)")
  featured_image_large = ImageSpecField(source="featured_image",
                       processors=[ResizeToFit(1280, 1280)],
                       format='JPEG'
                       )

  featured_image_medium = ImageSpecField(source='featured_image',
                      processors=[ResizeToFit(700, 700)],
                      format="JPEG",
                      options={'quality': 80}
                      )

  featured_image_small = ImageSpecField(source='featured_image',
                          processors=[ResizeToFill(250,250)],
                          format="JPEG",
                          options={'quality': 80}
                          )

  featured_image_thumbnail= ImageSpecField(source='featured_image',
                          processors=[ResizeToFill(75,75)],
                          format="JPEG",
                          options={'quality': 80}
                          )

  content = models.TextField(verbose_name="内容")
  # date_posted = models.DateTimeField(auto_now=True) #常に日付更新
  # date_posted = models.DateTimeField(auto_now_add=True) #作成時のみ更新。更新時日付更新されない。
  date_posted = models.DateTimeField(default=timezone.now)

  author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
  category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="posts", null=True, blank=True, verbose_name="カテゴリー(option)")
  tags = models.ManyToManyField(Tag, blank=True, related_name="posts", verbose_name="タグ(option)")
  draft = models.BooleanField(default=False, verbose_name="下書きにする")

  class Meta:
    verbose_name_plural = "投稿"

  def __str__(self):
    return self.title

  #編集後そのidのページに戻る
  def get_absolute_url(self):
      return reverse('post-detail', kwargs={'pk': self.pk})

  def approved_comments(self):
    return self.comments.filter(approved_comment=True)

  def links_ordered(self):
    return self.links.order_by('id')

  def comments_ordered(self):
    return self.comments.order_by('date_posted')

  # def published_post(self):
  #   if not self.draft:
  #     return 


class Comment(models.Model):
  comment = models.TextField(verbose_name="コメント")
  date_posted = models.DateTimeField(default=timezone.now)
  author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
  post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
  approved_comment = models.BooleanField(default=False)
  url = models.URLField(max_length=255, blank=True, verbose_name="参照URL(option)")

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


class URL(models.Model):
  title = models.CharField(max_length=100, blank=True, null=True, verbose_name="タイトル(option)")
  url = models.URLField(max_length=500, verbose_name="URL")
  post = models.ForeignKey(Post, blank=True, null=True, on_delete=models.CASCADE, related_name="links")

  class Meta:
    verbose_name_plural = "参照URL"

  def __str__(self):
    return self.url
