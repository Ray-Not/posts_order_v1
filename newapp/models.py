from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum


class Author(models.Model):
    AuthorUser = models.OneToOneField(User, on_delete=models.CASCADE)
    ratingAuthor = models.IntegerField(default=0)

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

    def __str__(self):
        return f'{self.AuthorUser.first_name} {self.AuthorUser.last_name}'


class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    NEWS = 'NW'
    ARTICLE = 'AR'
    CATEGORY_CHOICES = (
        (NEWS, 'Новость'),
        (ARTICLE, 'Статья'),
    )

    CategoryType = models.CharField(
        max_length=2,
        choices=CATEGORY_CHOICES,
        default=ARTICLE
    )
    dateCreation = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=128)
    text = models.TextField()
    rating = models.SmallIntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def __str__(self):
        return self.title


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    commentPost = models.ForeignKey(Post, on_delete=models.CASCADE)
    commentUser = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    dateCreation = models.DateTimeField(auto_now_add=True)
    rating = models.SmallIntegerField(default=0)

    def __str__(self):
        return self.commentUser.username

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()
