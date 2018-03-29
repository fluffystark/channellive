# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig


class UserprofileConfig(AppConfig):
    name = 'user_profile'

    def ready(self):
        import user_profile.signals
