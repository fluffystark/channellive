from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from UserProfile.models import Business


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


class UserRegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True,
                                   validators=[UniqueValidator(queryset=User.objects.all())])

    class Meta:
        model = User
        fields = ('username',
                  'password',
                  'first_name',
                  'last_name',
                  'email',)

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
