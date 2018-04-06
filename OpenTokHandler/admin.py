# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from OpenTokHandler.models import Livestream
from OpenTokHandler.models import Viewer
from OpenTokHandler.models import Archive
from OpenTokHandler.models import Report
from OpenTokHandler.models import ReportType
# Register your models here.


class ReportTypeInline(admin.TabularInline):
    model = ReportType
    extra = 1


class ReportAdmin(admin.ModelAdmin):

        fieldsets = [
            (None, {
                'fields': ('sentby',
                           'livestream',
                           'report_type',
                           'status',)
            }),
        ]
        list_display = ('sentby', 'livestream', 'status',)
        list_filter = ('livestream', 'sentby', 'status',)
        inline = [
            ReportTypeInline,
        ]


class ArchiveAdmin(admin.ModelAdmin):

        fieldsets = [
            (None, {
                'fields': ('livestream',
                           'archive',
                           'video',
                           'timestamp',
                           'thumbnail',)
            }),
        ]
        readonly_fields = ('timestamp',)
        list_display = ('livestream', 'timestamp', 'has_video')
        list_filter = ('livestream',)

        def has_video(self, obj):
            retval = False
            if obj.video is not None:
                retval = True
            return retval

        has_video.boolean = True


class LivestreamAdmin(admin.ModelAdmin):

        fieldsets = [
            (None, {
                'fields': ('user',
                           'event',
                           'is_live',
                           'session',
                           'archive',
                           'votes',
                           'thumbnail',)
            }),
        ]
        list_display = ('user', 'event', 'is_live')
        list_filter = ('user', 'event', 'is_live')


admin.site.register(Livestream, LivestreamAdmin)
admin.site.register(Viewer)
admin.site.register(Archive, ArchiveAdmin)
admin.site.register(Report, ReportAdmin)
