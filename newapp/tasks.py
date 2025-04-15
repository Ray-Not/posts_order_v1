from datetime import timedelta

from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone

from .models import Category, Post, User


@shared_task
def send_weekly_articles():
    week_ago = timezone.now() - timedelta(days=7)

    recent_posts = Post.objects.filter(
        dateCreation__gte=week_ago,
        is_sented=False
    )

    category_posts = {}

    for post in recent_posts:
        post.is_sented = True
        for category in post.categories.all():
            if category not in category_posts:
                category_posts[category] = []
            category_posts[category].append(post)

    Post.objects.bulk_update(recent_posts, ['is_sented'])

    for category, posts in category_posts.items():
        subscribers = category.subscribers.all()
        if subscribers.exists():
            articles_list = '\n'.join([
                f'• {post.title}: http://localhost:8000/news/{post.id}/'
                for post in posts
            ])

            for subscriber in subscribers:
                try:
                    send_mail(
                        subject=(f'Новые статьи за последнюю неделю '
                                 f'в категории {category.name}'),
                        message=(
                            f'Привет, {subscriber.username}!\n\n'
                            f'В категории «{category.name}» были опубликованы '
                            f'следующие новые статьи:\n\n'
                            f'{articles_list}\n\n'
                            f'Прочитай их, посетив сайт.'
                        ),
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[subscriber.email],
                        fail_silently=False,
                    )
                    print(f'Письмо отправлено подписчику {subscriber.email} о'
                          f'новых статьях в категории {category.name}')
                except Exception as e:
                    print(f'Ошибка при отправке письма '
                          f'подписчику {subscriber.email}: {e}')
        else:
            print(f'Нет подписчиков у категории {category.name}')


@shared_task
def send_welcome_email(user_id):
    try:
        user = User.objects.get(id=user_id)
        send_mail(
            'Добро пожаловать на наш сайт!',
            f'Привет, {user.first_name}!\n'
            f'Спасибо за регистрацию на нашем сайте.',
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )
        print(f'Письмо отправлено на {user.email}')
    except User.DoesNotExist:
        print(f'Пользователь с ID {user_id} не найден.')
    except Exception as e:
        print(f'Ошибка при отправке письма на {user.email}: {e}')


@shared_task
def send_post_notification(post_id, category_id):
    post = Post.objects.get(id=post_id)
    category = Category.objects.get(id=category_id)
    subscribers = category.subscribers.all()

    if subscribers.exists():
        for subscriber in subscribers:
            try:
                send_mail(
                    subject=f'Новый пост в категории {category.name}',
                    message=(
                        f'Привет, {subscriber.username}!\n\n'
                        f'В категории «{category.name}» '
                        f'появился новый пост: «{post.title}».\n'
                        f'{post.text[:50]}...\n\n'
                        f'Прочитай его по ссылке: '
                        f'http://localhost:8000/news/{post.id}/'
                    ),
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[subscriber.email],
                    fail_silently=False,
                )
                print(f'Письмо отправлено {subscriber.email}')
            except Exception as e:
                print(f'Ошибка при отправке письма {subscriber.email}: {e}')
    else:
        print(f'Нет подписчиков у категории {category.name}')
