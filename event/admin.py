# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline

from event.models import Event, Category
from PrizeHandler.models import Prize
from FileUpload.models import EventImage


class ImageInline(admin.TabularInline):
    model = EventImage
    extra = 1


class CategoryInline(admin.TabularInline):
    model = Category
    extra = 1


class EventInline(GenericTabularInline):
    model = Event
    extra = 1


class EventAdmin(admin.ModelAdmin):

    def check_status(self, obj):
        return obj.self_status()

    def first_prize(self, obj):
        return obj.prizes.filter(title="First Prize").user

    def second_prize(self, obj):
        return obj.prizes.filter(title="Second Prize").user

    def third_prize(self, obj):
        return obj.prizes.filter(title="Third Prize").user

    fieldsets = [
        (None, {
            'fields': ('name',
                       'description',
                       'category',
                       'business',
                       'image',
                       'budget',
                       'start_date',
                       'end_date',
                       'location',
                       'review',
                       'pub_date',
                       'check_status',
                       'first_prize',
                       'second_prize',
                       'third_prize',)
        }),
    ]
    readonly_fields = ('pub_date',
                       'check_status',
                       'first_prize',
                       'second_prize',
                       'third_prize',)
    inline = [
        CategoryInline,
        ImageInline,
    ]


admin.site.register(Event, EventAdmin)
admin.site.register(Category)
admin.site.register(Prize)
