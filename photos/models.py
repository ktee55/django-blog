from django.db import models
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


class Photo(models.Model):

  origin = models.ImageField(upload_to="photos/%y/%m/%d/")

  # large = ImageSpecField(source="origin",
  #                      processors=[ResizeToFill(1280, 1024)],
  #                      format='JPEG'
  #                      )

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

  author = models.ForeignKey(User, blank=True, on_delete=models.CASCADE, related_name="photos")

  private = models.BooleanField(default=False, verbose_name="非公開にする")

  category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="posts", null=True, blank=True, verbose_name="カテゴリー")

  tags = models.ManyToManyField(Tag, blank=True, related_name="posts", verbose_name="タグ")

  #編集後そのidのページに戻る
  def get_absolute_url(self):
      return reverse('photo-detail', kwargs={'pk': self.pk})