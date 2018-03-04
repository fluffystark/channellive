# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
# from rest_framework.views import APIView
from UserProfile.models import Business
from UserProfile.serializers import BusinessSerializer
from UserProfile.serializers import LoginSerializer
from UserProfile.serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request):
        data = request.data
        print data
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
            newUser = User.objects.create_user(username=data['username'],
                                               password=data['password'],
                                               first_name=data['first_name'],
                                               last_name=data['last_name'],
                                               email=data['email'],)
            print newUser
            if data['is_business']:
                new_biz = Business(user=newUser,
                                   company_name=data['business_name'])
                new_biz.save()
            content = {
                "statusCode": "201",
                "username": data['username'],
                "message": "Account Successfully Created",
            }
            stat = status.HTTP_201_CREATED
        return Response(content, stat)


class LoginViewSet(viewsets.ViewSet):
    queryset = User.objects.all()
    serializer_class = LoginSerializer

    def get_queryset(self):
        return self.request.user

    def create(self, request):
        obj = request.user
        is_business = Business.objects.filter(user=obj).exists()
        content = {'user_id': obj.id,
                   'username': obj.get_username(),
                   'is_business': is_business, }
        return Response(content, status=status.HTTP_200_OK)


class BusinessViewSet(viewsets.ModelViewSet):
    queryset = Business.objects.all()
    serializer_class = BusinessSerializer
