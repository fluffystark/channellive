# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
import pytz
from django.utils import timezone
from rest_framework import viewsets
from rest_framework.response import Response
from EventHandler.models import Event
from EventHandler.models import Category
from UserProfile.models import Business
from EventHandler.serializers import EventSerializer
from EventHandler.serializers import CategorySerializer


class EventViewSet(viewsets.ModelViewSet):
    serializer_class = EventSerializer

    def get_queryset(self):
        queryset = Event.objects.all()
        if self.request.query_params.get('business_id', None):
            pk = self.request.query_params.get('business_id', None)
            if Business.objects.filter(pk=pk).exists():
                business = Business.objects.get(pk=pk)
                queryset = queryset.filter(business=business)
        status = self.request.query_params.get('status', None)
        if status == 'incoming':
            queryset = queryset.filter(start_date__gt=timezone.now())
        elif status == 'ongoing':
            queryset = queryset.filter(start_date__lt=timezone.now(),
                                       end_date__gt=timezone.now())
        elif status == 'ended':
            queryset = queryset.filter(end_date__lt=timezone.now())
        return queryset

    def list(self, request):
        serializer = EventSerializer(self.get_queryset(), many=True)
        return Response(serializer.data)

    def create(self, request):
        data = request.data
        description = request.data['description']
        now = timezone.now()
        new_event = None
        start_date = data['start_date']
        content = None
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
            business = Business.objects.get(pk=data['business_id'])
            new_event = Event(business=business,
                              category=category,
                              description=description[:239],
                              name=data['name'],
                              budget=float(data['budget']),
                              start_date=parsed_start_date,
                              end_date=parsed_end_date,
                              )
            new_event.save()
            content = new_event.id
        else:
            content = -1
        return Response(content)


class HasEventViewSet(viewsets.ViewSet):

    def retrieve(self, request, pk=None):
        has_event = False
        if Business.objects.filter(pk=pk):
            business = Business.objects.get(pk=pk)
            if business.events.all().count() > 0:
                has_event = True
        content = has_event
        return Response(content)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
