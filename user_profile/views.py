# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User

from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from user_profile.models import Business
from user_profile.serializers import BusinessSerializer
from user_profile.serializers import UserRegistrationSerializer


class BusinessViewSet(viewsets.ModelViewSet):
    queryset = Business.objects.all()
    serializer_class = BusinessSerializer


class UserRegistrationViewSet(viewsets.ViewSet):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer

    def create(self, request):
        data = request.data
        user_serializer = UserRegistrationSerializer(data=data)
        content = {}
        if user_serializer.is_valid():
            new_user = user_serializer.save()
            business_id = -1
            if data['is_business'] == u'true':
                new_business = Business(user=new_user,
                                        company_name=data['business_name'])
                new_business.save()
                business_id = new_business.id
            content = {
                "statusCode": "201",
                "user_id": new_user.id,
                "username": new_user.username,
                "business_id": business_id,
                "message": "Account Successfully Created",
            }
            return Response(content, status.HTTP_201_CREATED)
        if 'username' in user_serializer.errors:
            content = "Username already exist"
        elif 'email' in user_serializer.errors:
            content = "Email already exist"
        return Response(content, status.HTTP_409_CONFLICT)


class LoginViewSet(viewsets.ViewSet):
    queryset = User.objects.all()

    def get_queryset(self):
        return self.request.user

    def create(self, request):
        obj = request.user
        business_id = -1
        business = Business.objects.filter(user=obj).first()
        if business is not None:
            business_id = business.pk
        content = {'user_id': obj.id,
                   'username': obj.get_username(),
                   'business_id': business_id, }
        return Response(content, status=status.HTTP_200_OK)
