from rest_framework import serializers
from OpenTokHandler.models import Livestream
from OpenTokHandler.models import Viewer


class LivestreamSerializer(serializers.ModelSerializer):
    livestream_id = serializers.SerializerMethodField('get_id')
    user_id = serializers.SerializerMethodField('get_user')
    event_id = serializers.SerializerMethodField('get_event')
    username = serializers.SerializerMethodField()

    class Meta:
        model = Livestream
        fields = ('livestream_id',
                  'user_id',
                  'event_id',
                  'is_live',
                  'username',
                  'session',
                  'votes',
                  'views')

    def get_id(self, obj):
        return obj.id

    def get_user(self, obj):
        return obj.user.pk

    def get_event(self, obj):
        return obj.event.pk

    def get_username(self, obj):
        return obj.user.username


class ViewerSerializer(serializers.ModelSerializer):
    user_id = serializers.SerializerMethodField('get_user')

    class Meta:
        model = Viewer
        fields = ('livestream_id',
                  'user_id',
                  'has_voted')

    def get_user(self, obj):
        return obj.user.pk
