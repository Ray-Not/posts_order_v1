from django.contrib import admin

from .models import Author, Comment, Post, Category

admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Author)
admin.site.register(Comment)
