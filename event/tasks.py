# Create your tasks here
from __future__ import absolute_import, unicode_literals

from django.conf import settings
from django.contrib.auth.models import User, Group
from django.db.models import Q
from django.utils import timezone
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
        if event.start_date < now < event.end_date:
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
        user.email_user(subject="Event for Approval",
                        message="Log in and approve the event \n\n" +
                                event.name + " \n\n http://192.168.254.60:8000" +
                                "/admin/event/event/" + str(event.id) +
                                "/change/\n\n" + "- Channel Live Team -",)
