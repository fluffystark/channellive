# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Notification(models.Model):
    message = models.CharField(max_length=200)
    user = models.ForeignKey(User,
                             related_name='notifications')
    unread = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)


class NotificationType(models.Model):
    text = models.CharField(max_length=50)

    def __str__(self):
        return self.text
