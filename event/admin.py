# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline

from event.models import Event, Category
from event.models import Prize


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
                       'verification_uuid',
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
    ]
    list_display = ('name', 'business', 'status', 'review')
    list_filter = ['status']


class PrizeAdmin(admin.ModelAdmin):

    fieldsets = [
        (None, {
            'fields': ('title',
                       'amount',
                       'event',
                       'user',)
        }),
    ]
    list_display = ('event', 'title', 'has_user',)
    list_filter = ('event',)

    def has_user(self, obj):
        retval = False
        if obj.user is not None:
            retval = True
        return retval

    has_user.boolean = True


admin.site.register(Event, EventAdmin)
admin.site.register(Category)
admin.site.register(Prize, PrizeAdmin)
