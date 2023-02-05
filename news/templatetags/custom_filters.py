from django import template

register = template.Library()


@register.filter()
def censor(value):
    """value: значение, к которому нужно применить фильтр."""
    filthy_list = ['редиска', 'ещеплохоеслово']

    if not isinstance(value, str):
        raise TypeError(f'unresolved type {type(value)}, expected type "str"')

    words = value.split()

    for word in words:
        if word in filthy_list:
            value = value.replace(word, f'{word[0]}{"*" * (len(word) - 1)}')
            return value
    return value
