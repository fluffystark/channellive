# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import list_route
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from notification.models import Notification
from user_profile.models import Business
from user_profile.models import UserProfile
from notification.serializers import NotificationSerializer
from user_profile.serializers import BusinessSerializer
from user_profile.serializers import UserRegistrationSerializer
from user_profile.serializers import UserSerializer


class BusinessViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = BusinessSerializer
    queryset = Business.objects.all()


class UserRegistrationViewSet(viewsets.ViewSet):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer

    def create(self, request):
        data = request.data
        user_serializer = UserRegistrationSerializer(data=data)
        content = {"statusCode": "409",
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
            content["message"] = "username"
        elif 'email' in user_serializer.errors:
            content["message"] = "email"
        return Response(content)


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
                   'business_id': business_id,
                   'is_verified': obj.userprofile.is_verified}
        return Response(content, status=status.HTTP_200_OK)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    @detail_route(methods=['get'])
    def count_notifications(self, request, pk=None):
        user = self.get_object()
        count = Notification.objects.filter(user=user,
                                            unread=True).count()
        return Response(count)

    @detail_route(methods=['get'])
    def notifications(self, request, pk=None):
        user = self.get_object()
        queryset = Notification.objects.filter(user=user)
        serializer = NotificationSerializer(queryset, many=True)
        return Response(serializer.data)

    @detail_route(methods=['get'])
    def verification(self, request, pk=None):
        code = self.request.query_params.get('code', None)
        print code
        user = UserProfile.objects.filter(user_id=pk).first()
        content = {
            "statusCode": "400",
            "statusType": "conflict",
            "message": "Account Verification Error",
        }
        print user.verification_code
        if user is not None and code == user.verification_code:
            user.is_verified = True
            user.save(update_fields=['is_verified'])
            content = {
                "statusCode": "201",
                "statusType": "success",
                "message": "Account Successfully Verified",
            }
        return Response(content)

    @detail_route(methods=['get'])
    def send_verification(self, request, pk=None):
        user = User.objects.filter(pk=pk).first()
        content = {
            "statusCode": "400",
            "statusType": "conflict",
            "message": "Email does not exist.",
        }
        if user is not None:
            content = {
                "statusCode": "201",
                "statusType": "success",
                "message": user.id,
            }
            user.userprofile.user_send_email_verification_now()
        return Response(content)

    @list_route(methods=['post'])
    def email_verification(self, request, pk=None):
        data = request.data
        user = User.objects.filter(email=data).first()
        content = {
            "statusCode": "400",
            "statusType": "conflict",
            "message": "Email does not exist.",
        }
        if user is not None:
            content = {
                "statusCode": "201",
                "statusType": "success",
                "message": user.id,
            }
            user.userprofile.user_send_email_verification_now()
        return Response(content)

    @list_route(methods=['post'])
    def set_password(self, request):
        data = request.data
        print data
        verification_code = data["verification_code"]
        password = data["password"]
        content = {
            "statusCode": "400",
            "statusType": "conflict",
            "message": "Wrong verification code sent.",
        }
        user = User.objects.filter(id=data["user_id"]).first()
        if user.userprofile.verification_code == str(verification_code):
            user.set_password(password)
            user.save()
            content = {
                "statusCode": "201",
                "statusType": "success",
                "message": "New password set.",
            }
        return Response(content)
