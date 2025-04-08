import re

from django import template

register = template.Library()

BAD_WORDS = ['мат',]


def censor(value):
    """Функция для цензурирования текста."""
    for word in BAD_WORDS:
        value = re.sub(
            r'\b' + re.escape(word) + r'\b',
            '*' * len(word),
            value,
            flags=re.IGNORECASE)
    return value


def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists()


register.filter('censor', censor)
register.filter('has_group', has_group)
