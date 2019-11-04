from django.contrib import admin

from .models import Photo, Category, Tag

class PhotoAdmin(admin.ModelAdmin):
    filter_horizontal = ("tags",)

class PhotoInline(admin.StackedInline):
    model = Photo.tags.through
    extra = 1

class TagAdmin(admin.ModelAdmin):
    inlines = [PhotoInline]

admin.site.register(Photo, PhotoAdmin)
admin.site.register(Category)
admin.site.register(Tag, TagAdmin)
