# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from OpenTokHandler.models import Livestream
from OpenTokHandler.models import Viewer
from OpenTokHandler.models import Archive
from OpenTokHandler.serializers import LivestreamSerializer
from OpenTokHandler.serializers import ViewerSerializer
from OpenTokHandler.serializers import ArchiveSerializer

from opentok import OpenTok
from opentok import Roles
from opentok import MediaModes

APIKey = settings.TOK_APIKEY
secretkey = settings.TOK_SECRETKEY
opentok = OpenTok(APIKey, secretkey)


class LivestreamViewSet(viewsets.ModelViewSet):
    serializer_class = LivestreamSerializer

    def get_queryset(self):
        queryset = Livestream.objects.all()
        event = self.request.query_params.get('event_id', None)
        isLive = self.request.query_params.get('is_live', None)
        if event is not None:
            queryset = Livestream.objects.filter(event=event)
        if isLive == u'true':
            queryset = queryset.filter(is_live=True)
        elif isLive == u'false':
            queryset = queryset.filter(is_live=False)
        return queryset

    def create(self, request):
        data = request.data
        session = opentok.create_session(media_mode=MediaModes.routed)
        session_id = session.session_id
        token = opentok.generate_token(session_id, Roles.publisher)
        livestream = Livestream.objects.filter(user_id=data['user_id'],
                                               event_id=data['event_id']).first()
        print livestream
        if livestream is None:
            livestream = Livestream(user_id=data['user_id'],
                                    event_id=data['event_id'],
                                    session=session_id,)
        else:
            livestream.session = session_id
            livestream.archive = ""

        livestream.save()
        content = {'SESSION_ID': session_id,
                   'TOKEN_PUBLISHER': token,
                   'API_KEY': APIKey,
                   'livestreamId': livestream.id}
        return Response(content)

    @detail_route(methods=['get'])
    def end(self, request, pk=None):
        livestreamer = self.get_object()
        livestreamer.is_live = False
        archive_id = str(livestreamer.archive)
        opentok.stop_archive(archive_id)
        archive = opentok.get_archive(archive_id)
        print archive.url
        livestreamer.save()
        content = {'statusCode': '200',
                   'statusType': 'Success',
                   'message': 'End Livestream'}
        return Response(content)

    @detail_route(methods=['get'])
    def status(self, request, pk=None):
        livestreamer = self.get_object()
        content = {'statusCode': '200',
                   'statusType': 'Success',
                   'message': 'Status Updated'}
        if livestreamer.archive == "":
            archive = opentok.start_archive(livestreamer.session,
                                            name=u'ChannelLive')
            livestreamer.archive = archive.id
            new_archive = Archive(livestream=livestreamer,
                                  archive=archive.id)
            livestreamer.is_live = True
            new_archive.save()
            livestreamer.save()
        else:
            livestreamer.is_live = not livestreamer.is_live
            livestreamer.save()
        return Response(content)

    @detail_route(methods=['get'])
    def previewlist(self, request, pk=None):
        livestreamer = self.get_object()
        archives = livestreamer.archives.all()[:3]
        serializer = ArchiveSerializer(archives, many=True)
        return Response(serializer.data)

    @detail_route(methods=['get'])
    def fulllist(self, request, pk=None):
        livestreamer = self.get_object()
        archives = livestreamer.archives.all()
        serializer = ArchiveSerializer(archives, many=True)
        return Response(serializer.data)


class SubscriberViewSet(viewsets.ModelViewSet):
    serializer_class = LivestreamSerializer
    queryset = Livestream.objects.all()

    def retrieve(self, request, pk=None):
        livestreamer = self.get_object()
        user_id = self.request.query_params.get('user_id', None)
        viewer = Viewer.objects.filter(livestream=livestreamer.id,
                                       user_id=user_id).first()
        if viewer is None:
            viewer = Viewer(livestream=livestreamer,
                            user_id=user_id)
            viewer.save()
        session_id = livestreamer.session
        token = opentok.generate_token(session_id, Roles.subscriber)
        content = {'SESSION_ID': session_id,
                   'TOKEN_SUBSCRIBER': token,
                   'API_KEY': APIKey,
                   'viewer_id': viewer.id,
                   'viewer_vote': viewer.vote}
        return Response(content)


class VoteViewSet(viewsets.ModelViewSet):
    serializer_class = ViewerSerializer
    queryset = Viewer.objects.all()

    def retrieve(self, request, pk=None):
        viewer = self.get_object()
        viewer.vote = not viewer.vote
        viewer.save()
        content = viewer.vote
        return Response(content)


class ArchiveViewSet(viewsets.ModelViewSet):
    serializer_class = ArchiveSerializer
    queryset = Archive.objects.all()
