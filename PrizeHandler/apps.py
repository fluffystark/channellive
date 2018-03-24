# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig


class PrizehandlerConfig(AppConfig):
    name = 'PrizeHandler'

    def ready(self):
        import PrizeHandler.signals
