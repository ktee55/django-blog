from django.contrib import admin
from .models import Post, Comment, Category, Tag, URL


class PostInline(admin.StackedInline):
    model = Post.tags.through
    extra = 1

class TagAdmin(admin.ModelAdmin):
    inlines = [PostInline]


class URLInline(admin.StackedInline):
    model = URL
    extra = 1

class PostAdmin(admin.ModelAdmin):
    filter_horizontal = ("tags",)
    inlines = [URLInline]


admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
admin.site.register(Category)
admin.site.register(Tag, TagAdmin)
admin.site.register(URL)
