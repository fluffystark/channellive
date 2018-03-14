from rest_framework import serializers
from UserProfile.models import Business
from EventHandler.models import Event


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
