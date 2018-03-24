# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone

from FileUpload.models import EventImage
from UserProfile.models import Business

REVIEW_CHOICES = {
    (1, ("Pending")),
    (2, ("Approved")),
    (3, ("Rejected"))
}


class Category(models.Model):
    text = models.CharField(max_length=25)

    def __str__(self):
        return self.text


class Event(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=240)
    category = models.ForeignKey(Category,
                                 related_name='events',
                                 default=1)
    business = models.ForeignKey(Business,
                                 related_name='events',
                                 blank=True,
                                 null=True,)
    image = models.OneToOneField(EventImage,
                                 on_delete=models.CASCADE,
                                 blank=True,
                                 related_name='event',
                                 null=True)
    budget = models.FloatField(default=100)
    pub_date = models.DateTimeField(auto_now_add=True, blank=True)
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    location = models.CharField(max_length=50,
                                default="Cebu",
                                blank=True,
                                null=True)
    review = models.SmallIntegerField(choices=REVIEW_CHOICES, default=1)

    def __str__(self):
        return self.name

    def self_status(self):
        now = timezone.localtime(timezone.now())
        status = 'NONE'
        if self.start_date is not None:
            if now < self.start_date:
                status = 'INCOMING'
            elif self.start_date < now < self.end_date:
                status = 'ONGOING'
            elif now >= self.end_date:
                status = 'ENDED'
        return status

    def __unicode__(self):
        return self.name

# add constants for each choices

# modelmanager