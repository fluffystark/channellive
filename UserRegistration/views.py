# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from UserProfile.models import Business
from UserRegistration.serializers import UserRegistrationSerializer


class UserRegistrationViewSet(viewsets.ViewSet):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer

    def create(self, request):
        data = request.data
        new_user = {
            'username': data['username'],
            'password': data['password'],
            'first_name': data['first_name'],
            'last_name': data['last_name'],
            'email': data['email'],
        }
        if User.objects.filter(username=new_user['username']).exists():
            content = {
                "statusCode": "409",
                "error": "Conflict",
                "message": "Username already exist"
            }
            stat = status.HTTP_409_CONFLICT
        elif User.objects.filter(email=new_user['email']).exists():
            content = {
                "statusCode": "409",
                "error": "Conflict",
                "message": "Email already exist"
            }
            stat = status.HTTP_409_CONFLICT
        else:
            business_id = -1
            newUser = User.objects.create_user(username=data['username'],
                                               password=data['password'],
                                               first_name=data['first_name'],
                                               last_name=data['last_name'],
                                               email=data['email'],)
            if data['is_business']:
                new_business = Business(user=newUser,
                                        company_name=data['business_name'])
                new_business.save()
                business_id = new_business.id
            content = {
                "statusCode": "201",
                "user_id": newUser.id,
                "username": data['username'],
                "business_id": business_id,
                "message": "Account Successfully Created",
            }
            stat = status.HTTP_201_CREATED
        return Response(content, stat)
