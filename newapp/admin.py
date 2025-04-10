from django.contrib import admin

from .models import Author, Category, Comment, Post, PostCategory


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    filter_horizontal = ('subscribers',)


class PostCategoryInline(admin.TabularInline):
    model = PostCategory
    extra = 1


class PostAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'author',
        'CategoryType',
        'dateCreation',
        'rating'
    )
    list_filter = ('CategoryType', 'categories')
    search_fields = ('title', 'text')
    inlines = [PostCategoryInline]


admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Author)
admin.site.register(Comment)
