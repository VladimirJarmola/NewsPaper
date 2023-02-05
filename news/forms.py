from django import forms
from django.core.exceptions import ValidationError

from .models import Post


class PostForm(forms.ModelForm):
    """Класс генерирует форму создания поста."""

    text = forms.CharField(min_length=20)

    class Meta:
        """Указываем какие поля модели Post использовать."""

        model = Post
        fields = ['author', 'category', 'heading', 'text']

    def clean(self):
        """Метод реализует проверку введенных данных."""
        cleaned_data = super().clean()
        heading = cleaned_data.get('heading')
        text = cleaned_data.get('text')

        if heading == text:
            raise ValidationError(
                "Описание не должно быть идентично названию."
            )

        return cleaned_data
