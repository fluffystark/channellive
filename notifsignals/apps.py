# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig


class NotifsignalsConfig(AppConfig):
    name = 'notifsignals'

    def ready(self):
        import notifsignals.signals
