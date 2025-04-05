from django import template
import re

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


register.filter('censor', censor)
