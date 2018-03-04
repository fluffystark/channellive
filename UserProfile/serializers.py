from django.contrib.auth.models import User
from rest_framework import serializers
from UserProfile.models import Business


class UserSerializer(serializers.ModelSerializer):
    is_business = serializers.SerializerMethodField(method_name='is_business')

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'first_name', 'last_name', 'email',)

    def is_business(self, obj):
        return Business.objects.filter(user=obj).exists()


class BusinessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Business
        fields = ('id', 'company_name', 'user')


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password',)
