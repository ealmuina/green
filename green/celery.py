import os

import django
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'green.settings')
django.setup()

app = Celery(
    'tasks',
    broker='redis://redis:6379/0',
    backend='redis://redis:6379/0'
)

app.conf.beat_schedule = {
    # 'poll-records': {
    #     'task': 'tasks.poll_records',
    #     'schedule': crontab(minute='*/10')
    # }
}
app.conf.task_time_limit = 1800  # timeout after 30 minutes
