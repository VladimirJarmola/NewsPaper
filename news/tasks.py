from celery import shared_task
from django.conf import settings
import datetime

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from .models import PostCategory, Post, Category

# Собираем посты за последнюю неделю
today = datetime.datetime.now()
last_week = today - datetime.timedelta(days=7)
posts = Post.objects.filter(datatime_of_creation__gte=last_week)
categories = set(posts.values_list('category__name_category', flat=True))
subscribers = set(Category.objects.filter(name_category__in=categories).values_list('subscribers__email',
                                                                                    flat=True))


# Еженедельная рассылка новых постов подписчикам
@shared_task
def send_weekly():
    html_content = render_to_string(
        'weekly_email.html',
        {
            'link': f'{settings.SITE_URL}',
            'posts': posts
        }
    )
    for email in subscribers:
        msg = EmailMultiAlternatives(
            subject='Новые статьи за неделю на нашем портале',
            body='',
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[email],
        )

        msg.attach_alternative(html_content, "text/html")
        msg.send()


# Рассылка информации о создании нового поста
@shared_task
def send_notifications(preview, heading, subscribers, pk):
    subscribers_list = PostCategory.objects.filter(post_id=pk).values_list(
        'category__subscribers__username',
        'category__subscribers__email'
    )

    for username, email in subscribers_list:
        html_content = render_to_string(
            'post_create_email.html',
            {
                'text': preview,
                'link': f'{settings.SITE_URL}/news/{pk}',
                'username': username,
            }
        )

        msg = EmailMultiAlternatives(
            subject=heading,
            body='',
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[email],
        )

        msg.attach_alternative(html_content, "text/html")
        msg.send()
