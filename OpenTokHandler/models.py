# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
from PIL import Image
from django.contrib.auth.models import User
from django.db import models
from event.models import Event
from django.conf import settings

# Create your models here.
STATUS_CHOICES = {
    (1, "PENDING"),
    (2, "APPROVED"),
    (3, "REJECTED")
}


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
    thumbnail = models.ImageField(upload_to='livestream_pic',
                                  blank=True,
                                  null=True)

    def __str__(self):
        name = self.user.username + "_" + self.event.name
        return name

    def save(self, *args, **kwargs):
        super(Livestream, self).save(*args, **kwargs)
        old_pic = self.thumbnail
        if old_pic.name is not None:
            length = len(self.thumbnail.name)
            if old_pic.name[length - 3:] == "png":
                myimage = Image.open(settings.MEDIA_ROOT + self.thumbnail.name)
                myimage = myimage.convert('RGB')
                file = settings.MEDIA_ROOT + old_pic.name[:length - 3]
                myimage.save(file + "jpeg", 'JPEG', quality=80)
                os.remove(old_pic.path)
                self.thumbnail = old_pic.name[:length - 3] + "jpeg"
                super(Livestream, self).save(*args, **kwargs)


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
    video = models.URLField(max_length=400, blank=True, default='')
    timestamp = models.DateTimeField(auto_now_add=True)
    thumbnail = models.ImageField(upload_to='archive_pic',
                                  blank=True,
                                  null=True)

    def save(self, *args, **kwargs):
        super(Archive, self).save(*args, **kwargs)
        old_pic = self.thumbnail
        if self.thumbnail.name is not None:
            print self.thumbnail.name is not None
            length = len(old_pic.name)
            if old_pic.name[length - 3:] == "png":
                myimage = Image.open(settings.MEDIA_ROOT + self.thumbnail.name)
                myimage = myimage.convert('RGB')
                file = settings.MEDIA_ROOT + old_pic.name[:length - 3]
                myimage.save(file + "jpeg", 'JPEG', quality=80)
                os.remove(old_pic.path)
                self.thumbnail = old_pic.name[:length - 3] + "jpeg"
                super(Archive, self).save(*args, **kwargs)


class ReportType(models.Model):
    text = models.CharField(max_length=50)

    def __str__(self):
        return self.text


class Report(models.Model):

    PENDING = 1
    APPROVED = 2
    REJECTED = 3

    sentby = models.ForeignKey(User, related_name='reports')
    livestream = models.ForeignKey(Livestream,
                                   related_name='reports',
                                   null=True)
    report_type = models.ForeignKey(ReportType,
                                    related_name='reports',
                                    default=1)
    status = models.SmallIntegerField(choices=STATUS_CHOICES, default=PENDING)
