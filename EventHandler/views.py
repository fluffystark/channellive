# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from .models import Event
from rest_framework import viewsets
from rest_framework.response import Response
from EventHandler.serializers import EventSerializer


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def list(self, request):
        queryset = Event.objects.all()
        serializer = EventSerializer(queryset, many=True)
        return Response(serializer.data)