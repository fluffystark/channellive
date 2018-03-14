# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
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
    serializer_class = EventSerializer

    def get_queryset(self):
        queryset = None
        if self.request.query_params.get('user_id', None):
            user_id = self.request.query_params.get('user_id', None)
            user = User.objects.get(pk=user_id)
            if Business.objects.filter(user=user).exists():
                business = Business.objects.filter(user=user)
                status = self.request.query_params.get('status', None)
                if status == 'incoming':
                    queryset = Event.objects.filter(company=business,
                                                    start_date__gt=timezone.now())
                elif status == 'ongoing':
                    queryset = Event.objects.filter(company=business,
                                                    start_date__lt=timezone.now(),
                                                    end_date__gt=timezone.now())
                elif status == 'ended':
                    queryset = Event.objects.filter(company=business,
                                                    end_date__lt=timezone.now())
        else:
            queryset = Event.objects.all()
            print queryset
        return queryset

    def list(self, request):
        serializer = EventSerializer(self.get_queryset(), many=True)
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
