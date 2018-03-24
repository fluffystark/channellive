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