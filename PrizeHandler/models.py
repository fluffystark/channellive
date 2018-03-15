# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
from EventHandler.models import Event


class Prize(models.Model):
    title = models.CharField(max_length=50)
    amount = models.FloatField(default=100)
    event = models.ForeignKey(Event, related_name='prizes', blank=True, null=True)
    user = models.ForeignKey(User, related_name='prizes', blank=True, null=True)
