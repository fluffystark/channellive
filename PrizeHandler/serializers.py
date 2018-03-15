from rest_framework import serializers
from PrizeHandler.models import Prize


class PrizeSerializer(serializers.ModelSerializer):
    event_id = serializers.SerializerMethodField()
    user_id = serializers.SerializerMethodField()

    class Meta:
        model = Prize
        fields = ('event_id',
                  'user_id',
                  'title',
                  'amount',)

    def get_user_id(self, obj):
        user = -1
        if obj.user is not None:
            user = obj.user.pk
        return user

    def get_event_id(self, obj):
        return obj.event.pk
