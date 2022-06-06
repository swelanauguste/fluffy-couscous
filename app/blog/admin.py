from django.contrib import admin

from .models import Post, PostStatus

admin.site.register(Post)
admin.site.register(PostStatus)