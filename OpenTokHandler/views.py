# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import views
from rest_framework.response import Response
from .serializers import TokSerializer

from opentok import OpenTok
# Create your views here.


APIKey = '46071302'
secretkey = 'e0f223ec5212013442e01225024bad8f5df9c596'
opentok = OpenTok(APIKey, secretkey)
session = opentok.create_session()


class OpenTokView(views.APIView):
    serializer_class = TokSerializer

    def post(self, request, format=None):
        session_id = session.session_id
        token = opentok.generate_token(session_id)
        content = {
            'apikey': APIKey,
            'session_id': session_id,
            'token': token, }
        return Response(content)
