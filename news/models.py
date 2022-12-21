from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.urls import reverse


class Author(models.Model):
    authorUser = models.OneToOneField(User, on_delete=models.CASCADE)
    rating_author = models.IntegerField(default=0)

    def update_rating(self):
        post_rating_set = self.post_set.aggregate(post=Sum('rating')).get('post')
        if post_rating_set is None:
            post_rating_set = 0

        comment_rating_set = self.authorUser.comment_set.aggregate(comm=Sum('rating')).get('comm')
        if comment_rating_set is None:
            comment_rating_set = 0

        sum_user_comments = 0
        for post in self.post_set.all():
            rating = post.comment_set.aggregate(comment=Sum('rating'))
            user_comments_rating = rating.get('comment')
            sum_user_comments += user_comments_rating

        self.rating_author = post_rating_set * 3 + comment_rating_set + sum_user_comments
        self.save()

    def __str__(self):
        return f'{self.authorUser}'


class Category(models.Model):
    name_category = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return f'{self.name_category.title()}'


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    NEWS = 'NW'
    PAPER = 'PR'
    CATEGORY_CHOICES = (
        (NEWS, 'Новость'),
        (PAPER, 'Статья'),
    )
    choices = models.CharField(max_length=2, choices=CATEGORY_CHOICES, default=NEWS)

    datatime_of_creation = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through='PostCategory')
    heading = models.CharField(max_length=128)
    text = models.TextField()
    rating = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.heading.title()}: {self.text[:20]}'

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.text[0:123] + '...'

    def get_absolute_url(self):
        return reverse('post', args=[str(self.id)])


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    comment = models.TextField()
    datatime_of_creation = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()
