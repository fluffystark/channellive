# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from UserProfile.serializers import UserSerializer
from UserProfile.models import Business

# Create your views here.


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
            User.objects.create_user(username=data['username'],
                                     password=data['password'],
                                     first_name=data['first_name'],
                                     last_name=data['last_name'],
                                     email=data['email'],)
            # if 
            new_biz = {
                # "id"
                # "company_name": 
            }
            content = {
                "statusCode": "201",
                "username": data['username'],
                "message": "Account Successfully Created",
            }
            stat = status.HTTP_201_CREATED
        return Response(content, stat)


class LoginView(APIView):

    def get(self, request, format=None):
        content = {
            'user': unicode(request.user),  # `django.contrib.auth.User` instance.
            'auth': unicode(request.auth),  # None
        }
        return Response(content)

    def post(self, request, format=None):
        obj = request.user
        is_business = Business.objects.filter(user=obj).exists()
        content = {'username': obj.get_username(),
                   'is_business': is_business, }
        return Response(content, status=status.HTTP_200_OK)
