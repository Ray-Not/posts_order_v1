from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, UpdateView
from django.contrib.auth.decorators import login_required
from .forms import PostForm
from .models import Author, Post
from django.contrib.auth.models import Group


def home_view(request):
    context = {}
    return render(request, 'default.html', context)


def news_list(request):
    posts = Post.objects.all().order_by('-id')
    paginator = Paginator(posts, 2)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj
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


def news_search(request):
    query_author = request.GET.get('author', '')
    query_date = request.GET.get('date', '')

    posts = Post.objects.all()

    if query_author:
        posts = posts.filter(author__author__username__icontains=query_author)

    if query_date:
        posts = posts.filter(dateCreation__date=query_date)

    posts = posts.order_by('-dateCreation')

    paginator = Paginator(posts, 2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'query_author': query_author,
        'query_date': query_date,
    }
    return render(request, 'news/search.html', context)


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'news/post_form.html'
    success_url = reverse_lazy('post_list')

    def dispatch(self, request, *args, **kwargs):
        if (
            not request.user.is_authenticated or
            not request.user.groups.filter(name='authors').exists()
        ):
            return redirect('/accounts/')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        author = Author.objects.get_or_create(author=self.request.user)[0]
        form.instance.author = author
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'news/post_form.html'

    def get_object(self, queryset=None):
        post = super().get_object(queryset)
        if post.author.author != self.request.user:
            raise PermissionDenied()
        return post

    def get_success_url(self):
        return reverse_lazy('post_detail', kwargs={'id': self.object.pk})

    def get_permission_denied_message(self):
        pass


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'news/post_confirm_delete.html'
    success_url = reverse_lazy('post_list')

    def get_object(self, queryset=None):
        post = super().get_object(queryset)
        if post.author.author != self.request.user:
            raise PermissionDenied()
        return post


@login_required
def become_author(request):
    authors_group, _ = Group.objects.get_or_create(name='authors')
    Author.objects.get_or_create(author=request.user, rating_author=0)
    request.user.groups.add(authors_group)
    return redirect('/accounts/')
