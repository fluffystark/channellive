# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.parsers import FileUploadParser
from FileUpload.serializers import FileSerializer
from FileUpload.models import EventImage
from EventHandler.models import Event

# Create your views here.


class FileUploadViewSet(viewsets.ViewSet):
    parser_class = (FileUploadParser)
    serializer_class = FileSerializer

    def create(self, request):
        obj = request.data
        content = "Event Created"
        if Event.objects.filter(pk=obj['event_id']):
            new_img = EventImage(file=obj['file'])
            new_img.save()
            event = Event.objects.get(pk=obj['event_id'])
            event.image = new_img
            event.save()
        return Response(content)

# move to eventhandler
