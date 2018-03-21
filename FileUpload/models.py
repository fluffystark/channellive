# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
# Create your models here.


class EventImage(models.Model):
    file = models.ImageField(upload_to='event_pic', blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.file.name
