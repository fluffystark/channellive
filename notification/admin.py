# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from notification.models import Notification


class NotificationAdmin(admin.ModelAdmin):

        fieldsets = [
            (None, {
                'fields': ('user',
                           'message',
                           'unread',
                           'timestamp',)
            }),
        ]
        readonly_fields = ('timestamp',)
        list_display = ('user', 'unread')
        list_filter = ('user', 'unread',)


admin.site.register(Notification, NotificationAdmin)
