# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import uuid
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db import models
from user_profile.tasks import send_email_verification as verify_email


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
    verification_code = models.CharField(max_length=4,
                                         validators=[RegexValidator(r'^\d{1,10}$')],
                                         null='',)
    profilepic = models.ImageField(upload_to='profile_pic',
                                   blank=True,
                                   null=True)

    def __str__(self):
        return self.user.username

    def user_send_email_verification_now(self):
        verify_email.delay(self.user.pk)
        return "Send Email Verification."
