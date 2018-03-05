# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from OpenTokHandler.models import Livestream
from OpenTokHandler.models import Viewer
# Register your models here.

admin.site.register(Livestream)
admin.site.register(Viewer)
