# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
from dateutil import tz
from django.db.models import Q
from django.utils import timezone
from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.decorators import parser_classes
from rest_framework.parsers import FileUploadParser
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from event.models import Event
from event.models import Category
from event.models import Prize
from user_profile.models import Business
from event.serializers import EventSerializer
from event.serializers import CategorySerializer
from event.serializers import PrizeSerializer
from event.serializers import EventDisplaySerializer


class EventViewSet(viewsets.ModelViewSet):
    serializer_class = EventSerializer

    def get_queryset(self):
        queryset = Event.objects.all()
        category_id = self.request.query_params.get('category', None)
        name = self.request.query_params.get('name', None)
        pk = self.request.query_params.get('business_id', None)
        status = self.request.query_params.get('status', None)
        review = self.request.query_params.get('review', None)
        start_date = self.request.query_params.get('startDate', None)
        end_date = self.request.query_params.get('endDate', None)
        business = Business.objects.filter(pk=pk).first()
        if business is not None:
            queryset = queryset.filter(business=business)
        category = Category.objects.filter(pk=category_id).first()
        if category != -1 and category is not None:
            queryset = queryset.filter(category=category)
        if name is not None:
            queryset = queryset.filter(name__contains=name)
        if status == 'incoming':
            queryset = queryset.filter(status=Event.INCOMING)
        elif status == 'ongoing':
            queryset = queryset.filter(status=Event.ONGOING)
        elif status == 'ended':
            queryset = queryset.filter(status=Event.ENDED)

        if review == 'pending':
            queryset = queryset.filter(review=Event.PENDING)
        elif review == 'approved':
            queryset = queryset.filter(review=Event.APPROVED)
        elif review == 'rejected':
            queryset = queryset.filter(review=Event.REJECTED)
        if start_date is not None or end_date is not None:
            if start_date is not None and end_date is not None:
                start_date = datetime.datetime.fromtimestamp(int(start_date) / 1000.0)
                end_date = datetime.datetime.fromtimestamp(int(end_date) / 1000.0)
                query = Q(start_date__gt=start_date) & Q(start_date__lt=end_date)
            elif start_date is not None:
                start_date = datetime.datetime.fromtimestamp(int(start_date) / 1000.0)
                query = Q(start_date__lt=start_date)
            elif end_date is not None:
                end_date = datetime.datetime.fromtimestamp(int(end_date) / 1000.0)
                query = Q(start_date__gt=end_date)
            queryset = queryset.filter(query)
        return queryset

    def list(self, request):
        serializer = EventSerializer(self.get_queryset(), many=True)
        return Response(serializer.data)

    def create(self, request):
        data = request.data
        content = None
        new_event = None
        now = timezone.now()
        description = data['description']
        start_date = data['start_date']
        end_date = data['end_date']
        new_tz = tz.gettz(data['time_zone'])
        parsed_start_date = datetime.datetime(start_date['year'],
                                              start_date['month'] + 1,
                                              start_date['dayOfMonth'],
                                              start_date['hourOfDay'],
                                              start_date['minute'],
                                              tzinfo=new_tz
                                              )
        parsed_end_date = datetime.datetime(end_date['year'],
                                            end_date['month'] + 1,
                                            end_date['dayOfMonth'],
                                            end_date['hourOfDay'],
                                            end_date['minute'],
                                            tzinfo=new_tz
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

    @detail_route(methods=['get'])
    def prizes(self, request, pk=None, *args):
        event = self.get_object()
        prizes = Prize.objects.filter(event=event)
        serializer = PrizeSerializer(prizes, many=True)
        return Response(serializer.data)

    @detail_route(methods=['post'])
    @parser_classes((FileUploadParser,))
    def image(self, request, pk=None):
        event = self.get_object()
        if 'file' in request.data:
            file = request.data['file']
            event.image = file
            event.save()
            content = {"statusCode": 200,
                       "message": "Image Uploaded",
                       "statusType": "success",
                       }
        else:
            content = {"statusCode": 409,
                       "message": "Problem with Image Upload",
                       "statusType": "conflict",
                       }
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


class PrizeViewSet(viewsets.ModelViewSet):
    queryset = Prize.objects.all()
    serializer_class = PrizeSerializer

# make fixtures
# check loaddata
# dumpdata


class ApprovalViewSet(viewsets.ModelViewSet):
    renderer_classes = [TemplateHTMLRenderer]
    queryset = Event.objects.all()
    serializer_class = EventDisplaySerializer
    template_name = 'event/request.html'

    def retrieve(self, request, pk=None):
        event = Event.objects.filter(verification_uuid=pk).first
        serializer = EventDisplaySerializer(event)
        return Response({'serializer': serializer, 'event': event})

    @detail_route(methods=['post'])
    def approve(self, request, pk=None):
        event = Event.objects.filter(verification_uuid=pk).first()
        content = None
        if event is not None:
            approval = request.data['Approval_val']
            if approval is not None:
                if approval == "Approve":
                    event.review = Event.APPROVED
                    content = "Approval Success"
                elif approval == "Reject":
                    event.review = Event.REJECTED
                    content = "Approval Rejected"
            event.save(update_fields=['review'])
            serializer = EventDisplaySerializer(event)
            return Response({'serializer': serializer, 'event': event, 'status': content})
