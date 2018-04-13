# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import uuid
import os
from PIL import Image
from django.contrib.auth.models import User
from django.conf import settings
from django.db import models
from user_profile.models import Business

REVIEW_CHOICES = {
    (1, "Pending"),
    (2, "Approved"),
    (3, "Rejected")
}

STATUS_CHOICES = {
    (1, "INCOMING"),
    (2, "ONGOING"),
    (3, "ENDED")
}


class Category(models.Model):
    text = models.CharField(max_length=25)

    def __str__(self):
        return self.text


class Event(models.Model):

    INCOMING = PENDING = 1
    ONGOING = APPROVED = 2
    ENDED = REJECTED = 3

    name = models.CharField(max_length=50)
    description = models.CharField(max_length=240)
    category = models.ForeignKey(Category,
                                 related_name='events',
                                 default=1)
    business = models.ForeignKey(Business,
                                 related_name='events')
    image = models.ImageField(upload_to='event_pic',
                              blank=True,
                              null=True)
    budget = models.FloatField(default=100)
    pub_date = models.DateTimeField(auto_now_add=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    location = models.CharField(max_length=50, default="Cebu")
    review = models.SmallIntegerField(choices=REVIEW_CHOICES, default=PENDING)
    status = models.SmallIntegerField(choices=STATUS_CHOICES, default=INCOMING)
    verification_uuid = models.UUIDField('Unique Verification UUID', default=uuid.uuid4)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name
      
    def save(self, *args, **kwargs):
        super(Event, self).save(*args, **kwargs)
        if self.image != "":
            if self.image.name is not None:
                length = len(self.image.name)
                old_pic = self.image
                myimage = Image.open(settings.MEDIA_ROOT + self.image.name)
                myimage = myimage.convert('RGB')
                if old_pic.name[length - 3:] != "jpeg":
                    file = settings.MEDIA_ROOT + old_pic.name[:length - 3]
                else:
                    file = settings.MEDIA_ROOT + old_pic.name[:length - 4]
                myimage.save(file + "jpeg", 'JPEG', quality=50)
                os.remove(old_pic.path)
                self.image = old_pic.name[:length - 3] + "jpeg"
                super(Event, self).save(*args, **kwargs)
      
      

class Prize(models.Model):
    title = models.CharField(max_length=50)
    amount = models.FloatField(default=100)
    event = models.ForeignKey(Event, related_name='prizes')
    user = models.ForeignKey(User,
                             related_name='prizes',
                             null=True)

    def __str__(self):
        return self.event.name + "_" + self.title


class Bookmark(models.Model):
    event = models.ForeignKey(Event,
                              related_name='bookmarks',)
    user = models.ForeignKey(User,
                             related_name='bookmarks',)
    is_bookmarked = models.BooleanField(default=True)

    def __str__(self):
        return str(self.event.name) + "_" + str(self.user.username)
