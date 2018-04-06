from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'channellive.settings')

app = Celery('channellive')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


app.conf.beat_schedule = {
    'update-status-every-single-minute': {
        'task': 'event.tasks.update_event_status',
        'schedule': crontab()
    },
    'update-video-every-single-minute': {
        'task': 'OpenTokHandler.tasks.update_video_url',
        'schedule': crontab()
    },
    'code-generator-every-hour': {
        'task': 'user_profile.tasks.verification_code_generator',
        'schedule': crontab(hour='*/1')
    }
}
