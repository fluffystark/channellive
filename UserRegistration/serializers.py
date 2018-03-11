from django.contrib.auth.models import User
from rest_framework import serializers
from UserProfile.models import Business


class UserRegistrationSerializer(serializers.ModelSerializer):
    is_business = serializers.SerializerMethodField(method_name='is_business')

    class Meta:
        model = User
        fields = ('username', 'password', 'first_name', 'last_name', 'email',)

    def is_business(self, obj):
        return Business.objects.filter(user=obj).exists()
