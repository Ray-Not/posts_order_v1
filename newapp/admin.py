from django.contrib import admin

from .models import Author, Comment, Post, PostCategory

admin.site.register(Post)
admin.site.register(PostCategory)
admin.site.register(Author)
admin.site.register(Comment)
