# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from user_profile.models import Business
from user_profile.models import UserProfile
# Register your models here.

# class UserProfileAdmin(admin.ModelAdmin):

#     def first_prize(self, obj):
#         return obj.prizes.filter(title="First Prize").user

#     def second_prize(self, obj):
#         return obj.prizes.filter(title="Second Prize").user

#     def third_prize(self, obj):
#         return obj.prizes.filter(title="Third Prize").user

#     fieldsets = [
#         (None, {
#             'fields': ('name',
#                        'description',
#                        'category',
#                        'business',
#                        'image',
#                        'budget',
#                        'start_date',
#                        'end_date',
#                        'verification_uuid',
#                        'location',
#                        'review',
#                        'pub_date',
#                        'status',
#                        'first_prize',
#                        'second_prize',
#                        'third_prize',)
#         }),
#     ]
#     readonly_fields = ('pub_date',
#                        'first_prize',
#                        'second_prize',
#                        'third_prize',)
#     inline = [
#         CategoryInline,
#     ]
#     list_display = ('name', 'business', 'status', 'review')
#     list_filter = ['status']

admin.site.register(Business)
admin.site.register(UserProfile)
