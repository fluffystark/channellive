# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User

from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from notification.models import Notification
from user_profile.models import Business
from notification.serializers import NotificationSerializer
from user_profile.serializers import BusinessSerializer
from user_profile.serializers import UserRegistrationSerializer


class BusinessViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = BusinessSerializer
    queryset = Business.objects.all()

    @detail_route(methods=['get'])
    def count_notifications(self, request, pk=None):
        business = self.get_object()
        count = Notification.objects.filter(user=business.user,
                                            unread=True).count()
        return Response(count)

    @detail_route(methods=['get'])
    def notifications(self, request, pk=None):
        business = self.get_object()
        queryset = Notification.objects.filter(user=business.user)
        serializer = NotificationSerializer(queryset, many=True)
        return Response(serializer.data)


class UserRegistrationViewSet(viewsets.ViewSet):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer

    def create(self, request):
        data = request.data
        user_serializer = UserRegistrationSerializer(data=data)
        content = {"statusCode": 409,
                   "message": None,
                   "statusType": "conflict",
                   "attribute": None
                   }
        if user_serializer.is_valid():
            new_user = user_serializer.save()
            business_id = -1
            if data['is_business'] is True:
                new_business = Business(user=new_user,
                                        company_name=data['business_name'])
                new_business.save()
                business_id = new_business.id
            auth = {'user_id': new_user.id,
                    'username': new_user.username,
                    'business_id': business_id, }
            content = {
                "statusCode": "201",
                "attribute": auth,
                "statusType": "success",
                "message": "Account Successfully Created",
            }
            return Response(content, status.HTTP_201_CREATED)
        if 'username' in user_serializer.errors:
            content["message"] = "Username already exist"
        elif 'email' in user_serializer.errors:
            content["message"] = "Email already exist"
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
