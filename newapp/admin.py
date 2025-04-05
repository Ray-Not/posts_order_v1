from django.contrib import admin
from .models import Post, PostCategory, Author, Comment

admin.site.register(Post)
admin.site.register(PostCategory)
admin.site.register(Author)
admin.site.register(Comment)
