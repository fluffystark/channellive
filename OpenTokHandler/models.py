# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
from event.models import Event

# Create your models here.


class Livestream(models.Model):
    user = models.ForeignKey(User,
                             related_name='livestreams',)
    event = models.ForeignKey(Event,
                              related_name='livestreams',)
    is_live = models.BooleanField(default=False)
    session = models.CharField(max_length=200)
    archive = models.CharField(max_length=200,
                               blank=True,
                               default='')
    votes = models.IntegerField(default=0)

    def __str__(self):
        name = self.user.username + "_" + self.event.name
        return name


class Viewer(models.Model):
    livestream = models.ForeignKey(Livestream, related_name='viewers')
    user = models.ForeignKey(User, related_name='viewers')
    vote = models.BooleanField(default=False)

    def __str__(self):
        name = self.user.username + "_" + self.livestream.event.name
        return name


class Archive(models.Model):
    livestream = models.ForeignKey(Livestream, related_name='archives')
    archive = models.CharField(max_length=200,
                               blank=True,
                               default='')
    video = models.URLField(max_length=200, blank=True, default='')
    timestamp = models.DateTimeField(auto_now_add=True)
