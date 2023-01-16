import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NewsPaper.settings')

app = Celery('NewsPaper')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'every_weekly_sender': {
        'task': 'news.tasks.send_weekly',
        'schedule': crontab(hour=9, minute=1, day_of_week='monday'),

    },
}
