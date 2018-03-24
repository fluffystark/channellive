# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from notification.models import Notification

admin.site.register(Notification)
