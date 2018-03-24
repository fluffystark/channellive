# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from UserProfile.models import Business
from UserLogin.serializers import LoginSerializer


class LoginViewSet(viewsets.ViewSet):
    queryset = User.objects.all()
    serializer_class = LoginSerializer

    def get_queryset(self):
        return self.request.user

    def create(self, request):
        obj = request.user
        business_id = -1
        if Business.objects.filter(user=obj).exists():
            business_id = Business.objects.get(user=obj).pk
        content = {'user_id': obj.id,
                   'username': obj.get_username(),
                   'business_id': business_id, }
        return Response(content, status=status.HTTP_200_OK)

# COMBINE WITH PROFILE AND REGISTRATION
# RENAME FOLDER SOMETHING_SOMETHING