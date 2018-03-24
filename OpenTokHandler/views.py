# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.response import Response
from EventHandler.models import Event
from OpenTokHandler.models import Livestream
from OpenTokHandler.models import Viewer
from OpenTokHandler.serializers import LivestreamSerializer
from OpenTokHandler.serializers import ViewerSerializer

from opentok import OpenTok
from opentok import Roles
from opentok import MediaModes
from django.conf import settings

APIKey = settings.TOK_APIKEY
secretkey = settings.TOK_SECRETKEY
opentok = OpenTok(APIKey, secretkey)


class LivestreamViewSet(viewsets.ModelViewSet):
    serializer_class = LivestreamSerializer

    def get_queryset(self):
        event = self.request.query_params.get('event_id', None)
        queryset = Livestream.objects.filter(event=event)
        isLive = self.request.query_params.get('is_live', None)
        print type(isLive)
        if isLive == u'true':
            queryset = queryset.filter(is_live=True)
        else:
            queryset = queryset.filter(is_live=False)
        return queryset

    def create(self, request):
        data = request.data
        # change objects to just _id
        event_used = Event.objects.get(pk=data['event_id'])
        session = opentok.create_session(media_mode=MediaModes.routed)
        session_id = session.session_id
        token = opentok.generate_token(session_id, Roles.publisher)
        user = User.objects.get(pk=data['user_id'])
        livestreamer = Livestream(user=user,
                                  event=event_used,
                                  session=session_id,
                                  )
        livestreamer.save()
        content = {'SESSION_ID': session_id,
                   'TOKEN_PUBLISHER': token,
                   'API_KEY': APIKey,
                   'livestreamId': livestreamer.id}
        return Response(content)


class SubscriberViewSet(viewsets.ModelViewSet):
    serializer_class = LivestreamSerializer
    queryset = Livestream.objects.all()

    def retrieve(self, request, pk=None):
        livestreamer = self.get_object()
        viewer = None
        if not Viewer.objects.filter(livestream=livestreamer.id,
                                     user=livestreamer.user.id).exists():
            viewer = Viewer(livestream=livestreamer,
                            user=livestreamer.user)
            viewer.save()
        else:
            viewer = Viewer.objects.get(livestream=livestreamer.id,
                                        user=livestreamer.user.id)
        session_id = livestreamer.session
        token = opentok.generate_token(session_id, Roles.subscriber)
        content = {'SESSION_ID': session_id,
                   'TOKEN_SUBSCRIBER': token,
                   'API_KEY': APIKey,
                   'viewer_id': viewer.id}
        return Response(content)


class VoteViewSet(viewsets.ModelViewSet):
    serializer_class = ViewerSerializer
    queryset = Viewer.objects.all()

    def retrieve(self, request, pk=None):
        viewer = self.get_object()
        viewer.vote = not viewer.vote
        viewer.save()
        content = "Success"
        return Response(content)


class EndStreamViewSet(viewsets.ModelViewSet):
    serializer_class = LivestreamSerializer
    queryset = Livestream.objects.all()

    def retrieve(self, request, pk=None):
        livestreamer = self.get_object()
        livestreamer.is_live = False
        livestreamer.save()
        content = "End"
        return Response(content)


class ArchiveViewSet(viewsets.ModelViewSet):
    serializer_class = LivestreamSerializer
    queryset = Livestream.objects.all()

    def retrieve(self, request, pk=None):
        livestreamer = self.get_object()
        content = {}
        if livestreamer.archive == "":
            archive = opentok.start_archive(livestreamer.session,
                                            name=u'ChannelLive')
            livestreamer.archive = archive.id
            livestreamer.is_live = True
            livestreamer.save()
        else:
            livestreamer.is_live = not livestreamer.is_live
            livestreamer.save()
        return Response(content)
