from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum


class Author(models.Model):
    author = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    rating_author = models.IntegerField(
        default=0,
        verbose_name='Рейтинг автора'
    )

    def update_rating(self):
        post_rating = self.post_set.aggregate(
            post_sum=Sum('rating')
        )['post_sum'] or 0
        post_rating_total = post_rating * 3
        author_comments_rating = (
            self.user.comment_set.aggregate(
                comment_sum=Sum('rating')
            )['comment_sum'] or 0
        )
        post_comments_rating = (
            Comment.objects
            .filter(post__author=self)
            .aggregate(
                post_comments_sum=Sum('rating')
            )['post_comments_sum'] or 0
        )
        self.rating = (
            post_rating_total
            + author_comments_rating
            + post_comments_rating
        )
        self.save()

    @property
    def username(self):
        return self.author.username

    def __str__(self):
        return f'{self.author.username}'

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'


class Category(models.Model):
    name = models.CharField(
        max_length=64,
        unique=True,
        verbose_name='Название'
    )
    subscribers = models.ManyToManyField(
        User,
        related_name='subscribed_categories',
        blank=True,
        verbose_name='Подписчики'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'категории'


class Post(models.Model):
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )
    NEWS = 'NW'
    ARTICLE = 'AR'
    CATEGORY_CHOICES = (
        (NEWS, 'Новость'),
        (ARTICLE, 'Статья'),
    )

    CategoryType = models.CharField(
        max_length=2,
        choices=CATEGORY_CHOICES,
        default=ARTICLE,
        verbose_name='Тип поста'
    )
    dateCreation = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField(
        Category,
        through='PostCategory',
        verbose_name='Категории'
    )
    title = models.CharField(
        max_length=128,
        verbose_name='Заголовок'
    )
    text = models.TextField(verbose_name='Содержание')
    rating = models.SmallIntegerField(default=0, verbose_name='Рейтинг')
    is_sented = models.BooleanField(default=False)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.post} {self.category}"


class Comment(models.Model):
    commentPost = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        verbose_name='Пост'
    )
    commentUser = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    text = models.TextField(verbose_name='Текст')
    dateCreation = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    rating = models.SmallIntegerField(
        default=0,
        verbose_name='Рейтинг'
    )

    def __str__(self):
        return self.commentUser.username

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
