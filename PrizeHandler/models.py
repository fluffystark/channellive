# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db import models
from EventHandler.models import Event


class Prize(models.Model):
    title = models.CharField(max_length=50)
    amount = models.FloatField(default=100)
    event = models.ForeignKey(Event,
                              related_name='prizes',
                              blank=True,
                              null=True)
    user = models.ForeignKey(User,
                             related_name='prizes',
                             blank=True,
                             null=True)

    def __str__(self):
        return self.event.name + "_" + self.title

    @receiver(post_save, sender=Event)
    def ensure_prize_exists(sender, **kwargs):
        if kwargs.get('created', False):
            newEvent = kwargs.get('instance')
            prize = newEvent.budget * .8
            firstPrize = Prize(title="First Prize",
                               amount=prize * .5,
                               event=newEvent,)
            secondPrize = Prize(title="Second Prize",
                                amount=prize * .3,
                                event=newEvent,)
            thirdPrize = Prize(title="Third Prize",
                               amount=prize * .2,
                               event=newEvent,)
            firstPrize.save()
            secondPrize.save()
            thirdPrize.save()
