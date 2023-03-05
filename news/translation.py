from .models import Category, Post
from modeltranslation.translator import register, TranslationOptions


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    """Регистрируем модель Category и указываем для перевода поле name_category"""
    fields = ('name_category',)


@register(Post)
class PostTranslationOptions(TranslationOptions):
    """Регистрируем модель Post и указываем для перевода поле name_category"""
    fields = ('heading', 'text', )

