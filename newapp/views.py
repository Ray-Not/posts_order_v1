from django.shortcuts import render, get_object_or_404
from .models import Post


def home_view(request):
    context = {}
    return render(request, 'default.html', context)


def news_list(request):
    posts = Post.objects.all().order_by('-id')
    context = {
        'posts': posts
    }
    return render(request, 'news/news.html', context)


def news_detail(request, id):
    post = get_object_or_404(Post, id=id)
    comments = post.comment_set.all()
    context = {
        'post': post,
        'comments': comments,
    }
    return render(request, 'news/news_detail.html', context)
