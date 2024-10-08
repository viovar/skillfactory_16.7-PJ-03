import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Portal.settings')

app = Celery('Portal')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()


# Определение расписания для задачи рассылки новостей
app.conf.beat_schedule = {
    'send-weekly-newsletter': {
        'task': 'news.tasks.send_weekly_newsletter',  # Путь к задаче
        'schedule': crontab(hour=8, minute=0, day_of_week=1),
    },
}