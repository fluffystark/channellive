# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import uuid
from PIL import Image
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.conf import settings
from django.db import models
from random import randint
from user_profile.tasks import send_email_verification


def code_generator():
        code = str(randint(0, 9))
        count = 0
        while count < 3:
            code += str(randint(0, 9))
            count += 1
        return code


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
                                         default=code_generator())
    profilepic = models.ImageField(upload_to='profile_pic',
                                   blank=True,
                                   null=True)
    bio = models.CharField(max_length=150, blank=True, default="")
    auth_uuid = models.UUIDField('Unique Verification UUID', default=uuid.uuid4)

    def __str__(self):
        return self.user.username

    def user_send_email_verification_now(self):
        send_email_verification.delay(self.user.pk)
        return "Send Email Verification."

    def save(self, *args, **kwargs):
        super(UserProfile, self).save(*args, **kwargs)
        if self.profilepic != "":
            if self.profilepic.name is not None:
                length = len(self.profilepic.name)
                old_pic = self.profilepic
                myimage = Image.open(settings.MEDIA_ROOT + self.profilepic.name)
                myimage = myimage.convert('RGB')
                file = settings.MEDIA_ROOT + old_pic.name[:length - 3]
                myimage.save(file + "jpeg", 'JPEG', quality=50)
                os.remove(old_pic.path)
                self.profilepic = old_pic.name[:length - 3] + "jpeg"
                super(UserProfile, self).save(*args, **kwargs)
