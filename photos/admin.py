from django.contrib import admin

from .models import Photo, Category, Tag

admin.site.register(Photo)
admin.site.register(Category)
admin.site.register(Tag)
