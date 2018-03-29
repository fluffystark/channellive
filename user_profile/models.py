# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import uuid
from django.contrib.auth.models import User
from django.db import models


class Business(models.Model):
    company_name = models.CharField(max_length=50)
    user = models.OneToOneField(User,
                                related_name='company',
                                )

    def __str__(self):
        return self.company_name


class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='userprofile',)
    is_verified = models.BooleanField(default=False)
    verification_uuid = models.UUIDField('Unique Verification UUID',
                                         default=uuid.uuid4)
    profilepic = models.ImageField(upload_to='profile_pic',
                                   blank=True,
                                   null=True)

    def __str__(self):
        return self.user.username
