from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, UpdateView

from .forms import CustomAuthenticationForm, CustomUserCreationForm, PostForm
from .models import Author, Post


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


def signup(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Аккаунт {username} успешно создан!')
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'news/auth/register.html', {'form': form})


def signin(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'news/auth/login.html', {'form': form})


def signout(request):
    if not request.user.is_authenticated:
        return redirect('home')
    logout(request)
    return render(request, 'news/auth/logout.html')


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'news/post_form.html'
    success_url = reverse_lazy('news_list')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
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
        return 'Some'


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'news/post_confirm_delete.html'
    success_url = reverse_lazy('post_list')

    def get_object(self, queryset=None):
        post = super().get_object(queryset)
        if post.author.author != self.request.user:
            raise PermissionDenied("У вас нет прав на удаление этого поста.")
        return post
