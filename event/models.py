# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone

from file_upload.models import Image
from user_profile.models import Business

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

    PENDING = 1
    APPROVED = 2
    REJECTED = 3

    name = models.CharField(max_length=50)
    description = models.CharField(max_length=240)
    category = models.ForeignKey(Category,
                                 related_name='events',
                                 default=1)
    business = models.ForeignKey(Business,
                                 related_name='events')
    image = models.OneToOneField(Image,
                                 blank=True,
                                 related_name='event',
                                 null=True)
    budget = models.FloatField(default=100)
    pub_date = models.DateTimeField(auto_now_add=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    location = models.CharField(max_length=50, default="Cebu")
    review = models.SmallIntegerField(choices=REVIEW_CHOICES, default=PENDING)

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



# modelmanager