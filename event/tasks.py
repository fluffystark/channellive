# Create your tasks here
from __future__ import absolute_import, unicode_literals

from django.conf import settings
from django.contrib.auth.models import User, Group
from django.utils import timezone
from rest_framework.reverse import reverse
from channellive.celery import app
from event.models import Event
from event.models import Prize
from OpenTokHandler.models import Livestream

from opentok import OpenTok

APIKey = settings.TOK_APIKEY
secretkey = settings.TOK_SECRETKEY
opentok = OpenTok(APIKey, secretkey)


@app.task
def update_event_status():
    now = timezone.now()
    for event in Event.objects.filter(status=Event.INCOMING):
        if event.start_date < now:
            event.status = Event.ONGOING
            event.save()
    for event in Event.objects.filter(status=Event.ONGOING):
        if now > event.end_date:
            livestreams = Livestream.objects.filter(event=event).order_by('-votes')
            prizes = Prize.objects.filter(event=event)
            for prize, livestream in zip(prizes, livestreams):
                archives = livestream.archives.all()
                for archive in archives:
                    obj = opentok.get_archive(archive.archive)
                    archive.video = obj.url
                    archive.save(update_fields=['video'])
                prize.user = livestream.user
                prize.save(update_fields=['user'])
            event.status = Event.ENDED
            event.save()


@app.task
def send_event_approval_request(event_id):
    event = Event.objects.get(id=event_id)
    group = Group.objects.filter(name='Admin')
    for user in User.objects.filter(groups=group):
        message = "EVENT FOR APPROVAL: \n\
                   Name: %s \n\
                   Description: %s \n\n\
                   Click the link below to APPROVE the event request.\n\n\
                   yuchipashe.me%s\n\n \
                   - Channel Live Team -" % \
                  (event.name, event.description,
                   reverse('request-detail', args=[str(event.verification_uuid)]))
        user.email_user(subject="Event for Approval",
                        message=message,)
