# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
import pytz
from django.conf import settings
from django.utils import timezone
from rest_framework import viewsets
from rest_framework.response import Response
from event.models import Event
from event.models import Category
from user_profile.models import Business
from event.serializers import EventSerializer
from event.serializers import CategorySerializer


class EventViewSet(viewsets.ModelViewSet):
    serializer_class = EventSerializer

    def get_queryset(self):
        queryset = Event.objects.all()
        status = self.request.query_params.get('status', None)
        pk = self.request.query_params.get('business_id', None)
        review = self.request.query_params.get('review', None)
        if Business.objects.filter(pk=pk).exists():
            business = Business.objects.get(pk=pk)
            queryset = queryset.filter(business=business)

        if status == 'incoming':
            queryset = queryset.filter(start_date__gt=timezone.now())
        elif status == 'ongoing':
            queryset = queryset.filter(start_date__lt=timezone.now(),
                                       end_date__gt=timezone.now())
        elif status == 'ended':
            queryset = queryset.filter(end_date__lt=timezone.now())

        if review == 'pending':
            queryset = queryset.filter(review=Event.PENDING)
        elif review == 'approved':
            queryset = queryset.filter(review=Event.APPROVED)
        elif review == 'rejected':
            queryset = queryset.filter(review=Event.REJECTED)
        return queryset

    def list(self, request):
        serializer = EventSerializer(self.get_queryset(), many=True)
        return Response(serializer.data)

    def create(self, request):
        data = request.data
        description = data['description']
        now = timezone.now()
        new_event = None
        start_date = data['start_date']
        content = None
        print start_date
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
            new_event = Event(category_id=data['category_id'],
                              business_id=data['business_id'],
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
        business = Business.objects.filter(pk=pk).first()
        if business is not None and business.events.all().count() > 0:
            has_event = True
        return Response(has_event)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

# make fixtures
# check loaddata
# dumpdata
# celery oh no
# fix timezone