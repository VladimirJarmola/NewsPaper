from django.contrib import admin
from django.db.models import F
from .models import Author, Category, Post, PostCategory, Comment
from modeltranslation.admin import TranslationAdmin


class CategoryAdmin(TranslationAdmin):
    """Регистрируем модель Category для перевода"""
    model = Category


class PostAdmin(TranslationAdmin):
    """Регистрируем модель Post для перевода"""
    model = Post


def rating_up(modeladmin, request, queryset):
    queryset.update(rating=F('rating') + 1)


def rating_down(modeladmin, request, queryset):
    queryset.update(rating=F('rating') - 1)


rating_up.short_description = 'Увеличить рейтинг'
rating_down.short_description = 'Уменьшить рейтинг'


class PostAdmin(admin.ModelAdmin):
    list_display = ('author', 'choices', 'datatime_of_creation', 'heading', 'rating',)
    list_filter = ('author', 'choices', 'datatime_of_creation', 'category__name_category')
    search_fields = ('heading', 'category__name_category')
    actions = [rating_up, rating_down]


admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Post, PostAdmin)
admin.site.register(PostCategory)
admin.site.register(Comment)
