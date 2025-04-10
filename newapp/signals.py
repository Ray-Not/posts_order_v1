from django.contrib.auth.models import Group, User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Author, PostCategory
from .tasks import send_welcome_email, send_post_notification


@receiver(post_save, sender=User)
def add_user_to_group(sender, instance, created, **kwargs):
    if created:
        common_group, _ = Group.objects.get_or_create(name='common')
        instance.groups.add(common_group)
        instance.save()


@receiver(post_save, sender=Author)
def add_user_to_authors_group(sender, instance, created, **kwargs):
    if created:
        authors_group, _ = Group.objects.get_or_create(name='authors')
        instance.author.groups.add(authors_group)


@receiver(post_save, sender=User)
def send_welcome_email_on_registration(sender, instance, created, **kwargs):
    if created:
        send_welcome_email.delay(instance.id)


@receiver(post_save, sender=PostCategory)
def send_post_notification_on_creation(sender, instance, created, **kwargs):
    if created:
        send_post_notification.delay(instance.post.id, instance.category.id)
