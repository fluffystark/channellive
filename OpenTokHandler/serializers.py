from rest_framework import serializers
from OpenTokHandler.models import Livestream


class TokSerializer(serializers.Serializer):
    session_id = serializers.CharField()

    class Meta:
        fields = ('session_id')


class LivestreamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Livestream
        fields = ('user',
                  'event',
                  'is_live',
                  'session',
                  'votes',
                  'views')
