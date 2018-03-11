# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.utils import timezone
import datetime
import pytz
from rest_framework import viewsets
from rest_framework.response import Response
from EventHandler.models import Event
from EventHandler.models import Category
from UserProfile.models import Business
from EventHandler.serializers import EventSerializer
from EventHandler.serializers import CategorySerializer


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def list(self, request):
        queryset = Event.objects.all()
        serializer = EventSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        data = request.data
        now = timezone.now()
        new_event = None
        start_date = data['start_date']
        parsed_start_date = datetime.datetime(start_date['year'],
                                              start_date['month'] + 1,
                                              start_date['dayOfMonth'],
                                              start_date['hourOfDay'],
                                              start_date['minute'],
                                              tzinfo=pytz.UTC
                                              )
        end_date = data['end_date']
        parsed_end_date = datetime.datetime(end_date['year'],
                                            end_date['month'] + 1,
                                            end_date['dayOfMonth'],
                                            end_date['hourOfDay'],
                                            end_date['minute'],
                                            tzinfo=pytz.UTC
                                            )
        if now <= parsed_start_date < parsed_end_date:
            category = Category.objects.get(pk=data['category_id'])
            company = Business.objects.get(pk=data['business_id'])
            new_event = Event(company=company,
                              category=category,
                              description=data['description'],
                              name=data['name'],
                              budget=float(data['budget'][1:]),
                              start_date=parsed_start_date,
                              end_date=parsed_end_date,
                              )
            new_event.save()
            content = {
                "statusCode": "201",
                "message": "Event is currently pending",
            }
        else:
            content = {
                "statusCode": "409",
                "message": "Error in date inputted",
            }
        return Response(content)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
