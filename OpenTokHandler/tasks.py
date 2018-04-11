# Create your tasks here
from __future__ import absolute_import, unicode_literals

from django.conf import settings
from django.utils import timezone
from django.db.models import Q
from channellive.celery import app
from OpenTokHandler.models import Archive


from opentok import OpenTok

APIKey = settings.TOK_APIKEY
secretkey = settings.TOK_SECRETKEY
opentok = OpenTok(APIKey, secretkey)


@app.task
def update_video_url():
    now = timezone.now()
    for archive in Archive.objects.filter(~Q(video=None)):
        archive.timestamp = now
        archive.video = opentok.get_archive(archive.archive).url
        if archive.video is not None:
            archive.save(update_fields=['timestamp', 'video'])
