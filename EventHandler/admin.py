# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from .models import Event, Category
# Register your models here.


class CategoryInline(admin.TabularInline):
    model = Category
    extra = 1


class EventInline(GenericTabularInline):
    model = Event
    extra = 1


class EventAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {
            'fields': ('name',
                       'description',
                       'category',
                       'company',
                       'budget',
                       'start_date',
                       'end_date',
                       'image',
                       'location',)
        }),
    ]
    inline = [
        CategoryInline,
    ]

    def check_status(self, obj):
        return obj.self_status()


admin.site.register(Event, EventAdmin)
admin.site.register(Category)
