# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from user_profile.models import Business
from user_profile.models import UserProfile
# Register your models here.


admin.site.register(Business)
admin.site.register(UserProfile)
