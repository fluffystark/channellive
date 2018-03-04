from django.contrib.auth.models import User
from rest_framework import serializers
from UserProfile.models import Business


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password', 'first_name', 'last_name', 'email')


class BusinessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Business
        fields = ('company_name', 'user')


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password',)
