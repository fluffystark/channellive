# Create your tasks here
from __future__ import absolute_import, unicode_literals

from django.utils import timezone
from channellive.celery import app
from event.models import Event


@app.task
def update_event_status():
    now = timezone.now()
    for event in Event.objects.filter(status=Event.INCOMING):
        if event.start_date < now < event.end_date:
            event.status = Event.ONGOING
            event.save()
    for event in Event.objects.filter(status=Event.ONGOING):
        if now > event.end_date:
            event.status = Event.ENDED
            event.save()
