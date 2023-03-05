from django import template
from django.utils import timezone

register = template.Library()


@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
    """Тэг для совместной работы фильтрации и пагинации."""
    d = context['request'].GET.copy()
    for k, v in kwargs.items():
        d[k] = v
    return d.urlencode()


@register.simple_tag()
def get_hour():
    """Тэг возвращает числовое значение текущего часа, для реализации смены темного/светлого фона"""
    now = timezone.localtime(timezone.now())
    return int(now.strftime('%H'))
