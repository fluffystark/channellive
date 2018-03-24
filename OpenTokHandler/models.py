# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
from event.models import Event

# Create your models here.


class Livestream(models.Model):
    user = models.ForeignKey(User,
                             related_name='livestreams',
                             blank=True,
                             default='')
    event = models.ForeignKey(Event,
                              related_name='livestreams',
                              blank=True,
                              default='')
    is_live = models.BooleanField(default=False)
    session = models.CharField(max_length=200)
    archive = models.CharField(max_length=200,
                               blank=True,
                               default='')

    def __str__(self):
        name = self.user.username + "_" + self.event.name
        return name


class Viewer(models.Model):
    livestream = models.ForeignKey(Livestream,
                                   related_name='viewers',
                                   blank=True,
                                   default='')
    user = models.ForeignKey(User,
                             related_name='viewers',
                             blank=True,
                             default='')
    vote = models.BooleanField(default=False)
