import os

import django
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'green.settings')
django.setup()

app = Celery(
    'tasks',
    broker='redis://green-redis:6379/0',
    backend='redis://green-redis:6379/0'
)

app.conf.beat_schedule = {
    'refresh-node-settings': {
        'task': 'web.tasks.refresh_node_settings',
        'schedule': crontab(hour='1')
    }
}
app.conf.task_time_limit = 3600  # timeout after 1 hour
