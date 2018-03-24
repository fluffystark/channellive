# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models


class Business(models.Model):
    company_name = models.CharField(max_length=50)
    user = models.OneToOneField(
        User,
        related_name='company',
    )

    def __str__(self):
        return self.company_name
