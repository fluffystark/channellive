# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import views
from rest_framework import viewsets
from rest_framework.response import Response
from OpenTokHandler.models import Livestream
from OpenTokHandler.serializers import TokSerializer
from OpenTokHandler.serializers import LivestreamSerializer

from opentok import OpenTok
# Create your views here.

# api key on settings

APIKey = '46071302'
secretkey = 'e0f223ec5212013442e01225024bad8f5df9c596'
opentok = OpenTok(APIKey, secretkey)


class OpenTokView(views.APIView):
    serializer_class = TokSerializer

    def post(self, request, format=None):
        session = opentok.create_session()
        session_id = session.session_id
        token = opentok.generate_token(session_id)
        content = {
            'apikey': APIKey,
            'session_id': session_id,
            'token': token, }
        return Response(content)


class LivestreamViewSet(viewsets.ViewSet):
    serializer_class = LivestreamSerializer

    def create(self, request):
        data = request.data
        if Livestream.objects.filter(
           user=request.user
           ).filter(
            event=data['event']
        ).exists():

        else:
            session = opentok.create_session()
            session_id = session.session_id
            token = opentok.generate_token(session_id)
            new_livestream = Livestream(user=request.user,
                                        event=data['event'],
                                        session=session_id,
                                        )
