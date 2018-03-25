# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline

from event.models import Event, Category
from event.models import Prize
from file_upload.models import Image


class ImageInline(admin.TabularInline):
    model = Image
    extra = 1


class CategoryInline(admin.TabularInline):
    model = Category
    extra = 1


class EventInline(GenericTabularInline):
    model = Event
    extra = 1


class EventAdmin(admin.ModelAdmin):

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
                       'status',
                       'first_prize',
                       'second_prize',
                       'third_prize',)
        }),
    ]
    readonly_fields = ('pub_date',
                       'first_prize',
                       'second_prize',
                       'third_prize',)
    inline = [
        CategoryInline,
        ImageInline,
    ]
    list_filter = ['status']


admin.site.register(Event, EventAdmin)
admin.site.register(Category)
admin.site.register(Prize)
admin.site.register(Image)
