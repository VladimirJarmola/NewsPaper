from django.forms import DateTimeInput
from django_filters import DateTimeFilter, FilterSet

from .models import Post


class PostFilter(FilterSet):
    """Набор фильтров для модели Post."""

    added_after = DateTimeFilter(
        field_name='datatime_of_creation',
        lookup_expr='gt',
        widget=DateTimeInput(
            format='%Y-%m-%dT%H:%M',
            attrs={'type': 'datetime-local'},
        ),
    )

    class Meta:
        """Описываем по каким полям модели будет производиться фильтрация."""

        model = Post
        fields = {
            'heading': ['icontains'],
            'category': ['exact'],

        }
