import os
import socket
from datetime import timedelta

from django.conf import settings

from celery import Celery
from kombu import Queue

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')

app = Celery(
    main='auction',
    backend=settings.CELERY_BACKEND,
    broker=settings.CELERY_BROKER
)

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.task_queues = (
    Queue(settings.CELERY_TASK_DEFAULT_QUEUE),
    Queue(socket.gethostname(), expires=60*60*24),
)

app.conf.timezone = 'UTC'

app.conf.CELERYBEAT_SCHEDULE = {
    'deactivate_expired_lots_every_minute': {
        'task': 'apps.marketplace.tasks.deactivate_expired_lots',
        'schedule': timedelta(minutes=1),
    },
}
