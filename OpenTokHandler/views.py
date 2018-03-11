# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.response import Response
from EventHandler.models import Event
from OpenTokHandler.models import Livestream
from OpenTokHandler.models import Viewer
from OpenTokHandler.serializers import LivestreamSerializer

from opentok import OpenTok
from opentok import Roles
from opentok import MediaModes
from django.conf import settings
# Create your views here.

# api key on settings

APIKey = settings.TOK_APIKEY
secretkey = settings.TOK_SECRETKEY
opentok = OpenTok(APIKey, secretkey)


class LivestreamViewSet(viewsets.ModelViewSet):
    serializer_class = LivestreamSerializer

    def get_queryset(self):
        event = self.request.query_params.get('event_id', None)
        return Livestream.objects.filter(is_live=True, event=event)

    def create(self, request):
        data = request.data
        print data
        if Livestream.objects.filter(user=data['user_id'], event=data['event_id']).exists():
            livestreamer = Livestream.objects.get(event=data['event_id'], user=data['user_id'])
            session_id = livestreamer.session
            token = opentok.generate_token(session_id, Roles.publisher)
            content = {'SESSION_ID': session_id,
                       'TOKEN_PUBLISHER': token,
                       'API_KEY': APIKey}
        else:
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
                       'API_KEY': APIKey}
        return Response(content)


class SubscriberViewSet(viewsets.ModelViewSet):
    serializer_class = LivestreamSerializer
    queryset = Livestream.objects.all()

    def retrieve(self, request, pk=None):
        livestreamer = self.get_object()
        if not Viewer.objects.filter(livestream=livestreamer.id, user=livestreamer.user.id).exists():
            viewer = Viewer(livestream=livestreamer,
                            user=livestreamer.user)
            viewer.save()
        session_id = livestreamer.session
        token = opentok.generate_token(session_id, Roles.subscriber)
        content = {'SESSION_ID': session_id,
                   'TOKEN_SUBSCRIBER': token,
                   'API_KEY': APIKey}
        return Response(content)
