# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
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

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name


class Prize(models.Model):
    title = models.CharField(max_length=50)
    amount = models.FloatField(default=100)
    event = models.ForeignKey(Event, related_name='prizes')
    user = models.ForeignKey(User,
                             related_name='prizes',
                             null=True)

    def __str__(self):
        return self.event.name + "_" + self.title

# modelmanager