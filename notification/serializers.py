from rest_framework import serializers
from notification.models import Notification
import datetime


class NotificationSerializer(serializers.ModelSerializer):
    timestamp = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = ('message',
                  'unread',
                  'timestamp',)

    def get_timestamp(self, obj):
        epoch = datetime.datetime.utcfromtimestamp(0)
        naive = obj.timestamp.replace(tzinfo=None)
        ms = long((naive - epoch).total_seconds() * 1000)
        # time = datetime.datetime.fromtimestamp(ms / 1000.0)
        return ms
