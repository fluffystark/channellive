# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.utils import timezone
from dateutil.parser import parse
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
        print parse(data['start_date'])
        if now <= parse(data['start_date']) < parse(data['end_date']):
            category = Category.objects.get(pk=data['category_id'])
            company = Business.objects.get(pk=data['business_id'])
            new_event = Event(company=company,
                              category=category,
                              description=data['description'],
                              name=data['name'],
                              budget=data['budget'],
                              start_date=data['start_date'],
                              end_date=data['end_date'],
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
