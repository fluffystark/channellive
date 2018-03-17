# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from EventHandler.models import Event
# Create your models here.


class EventImage(models.Model):
    file = models.ImageField(upload_to='event_pic', blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    event = models.OneToOneField(
        Event,
        on_delete=models.CASCADE,
        blank=True,
        related_name='eventimage',
        null=True
    )
