from django.contrib.auth.models import Group
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Author


@receiver(post_save, sender=User)
def add_user_to_group(sender, instance, created, **kwargs):
    if created:
        common_group = Group.objects.get(name='common')
        instance.groups.add(common_group)
        instance.save()


@receiver(post_save, sender=Author)
def add_user_to_authors_group(sender, instance, created, **kwargs):
    if created:
        authors_group, _ = Group.objects.get_or_create(name='authors')
        instance.author.groups.add(authors_group)
