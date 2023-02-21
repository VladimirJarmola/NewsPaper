from django.contrib.auth.models import User
from django.core.cache import cache
from django.db import models
from django.db.models import Sum
from django.urls import reverse


class Author(models.Model):
    """Модель авторов постов."""

    authorUser = models.OneToOneField(User, on_delete=models.CASCADE)
    rating_author = models.IntegerField(default=0)

    def update_rating(self):
        """Метод подсчитывает рейтинг Авторов."""
        post_rating_set = self.post_set.aggregate(
            post=Sum('rating')
        ).get('post')
        if post_rating_set is None:
            post_rating_set = 0

        comment_rating_set = self.authorUser.comment_set.aggregate(
            comm=Sum('rating')
        ).get('comm')
        if comment_rating_set is None:
            comment_rating_set = 0

        sum_user_comments = 0
        for post in self.post_set.all():
            rating = post.comment_set.aggregate(
                comment=Sum('rating')
            )
            user_comments_rating = rating.get('comment')
            sum_user_comments += user_comments_rating

        self.rating_author = post_rating_set * 3 \
            + comment_rating_set + sum_user_comments
        self.save()

    def __str__(self):
        """Метод для отображения информации об объекте класса."""
        return f'{self.authorUser}'


class Category(models.Model):
    """Модель категорий постов."""

    name_category = models.CharField(max_length=64, unique=True)
    subscribers = models.ManyToManyField(User, related_name='categories')

    def __str__(self):
        """Метод для отображения информации об объекте класса."""
        return f'{self.name_category}'


class Post (models.Model):
    """Модель постов."""

    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    NEWS = 'NW'
    PAPER = 'PR'
    CATEGORY_CHOICES = (
        (NEWS, 'Новость'),
        (PAPER, 'Статья'),
    )
    choices = models.CharField(
        max_length=2, choices=CATEGORY_CHOICES, default=NEWS
    )

    datatime_of_creation = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through='PostCategory')
    heading = models.CharField(max_length=128)
    text = models.TextField()
    rating = models.IntegerField(default=0)

    def __str__(self):
        """Метод для отображения информации об объекте класса."""
        return f'{self.heading.title()}: {self.text[:20]}'

    def like(self):
        """Метод увеличивающий поле rating на 1."""
        self.rating += 1
        self.save()

    def dislike(self):
        """Метод уменьшающий поле rating на 1."""
        self.rating -= 1
        self.save()

    def preview(self):
        """Метод реализующий предпросмотр поста."""
        return self.text[0:50] + '...'

    def get_absolute_url(self):
        """Метод возвращает уникальную ссылку на пост."""
        return reverse('post', args=[str(self.id)])

    def save(self, *args, **kwargs):
        """Метод удаляет из кэша пост при его изменении."""
        super().save(*args, **kwargs)
        cache.delete(f'post-{self.pk}')


class PostCategory(models.Model):
    """Промежуточная таблица для моделей Post и\
    Category связанных многие-ко-многим."""

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        """Метод для отображения информации об объекте класса."""
        return f'{self.post.heading.title()}  {self.category.name_category.title()}'


class Comment(models.Model):
    """Модель для хранения комментариев."""

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    comment = models.TextField()
    datatime_of_creation = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        """Метод увеличивающий поле rating на 1."""
        self.rating += 1
        self.save()

    def dislike(self):
        """Метод уменьшающий поле rating на 1."""
        self.rating -= 1
        self.save()

    def __str__(self):
        """Метод для отображения информации об объекте класса."""
        return f'{self.comment.title()}: {self.text[:20]}'
