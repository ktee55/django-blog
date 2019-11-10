from django.contrib import admin
from .models import Post, Comment, Category, Tag


class PostAdmin(admin.ModelAdmin):
    filter_horizontal = ("tags",)


class PostInline(admin.StackedInline):
    model = Post.tags.through
    extra = 1

class TagAdmin(admin.ModelAdmin):
    inlines = [PostInline]


admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
admin.site.register(Category)
admin.site.register(Tag, TagAdmin)
