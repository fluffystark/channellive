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
    business_id = serializers.SerializerMethodField('get_id')
    user_id = serializers.SerializerMethodField('get_user')
    business_name = serializers.SerializerMethodField('get_name')

    class Meta:
        model = Business
        fields = ('business_id',
                  'user_id',
                  'business_name',)

    def get_id(self, obj):
        return obj.id

    def get_user(self, obj):
        return obj.user.pk

    def get_name(self, obj):
        return obj.company_name


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password',)
