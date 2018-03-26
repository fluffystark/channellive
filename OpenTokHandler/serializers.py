from django.conf import settings
from rest_framework import serializers
from OpenTokHandler.models import Livestream
from OpenTokHandler.models import Viewer
from OpenTokHandler.models import Archive

from opentok import OpenTok

APIKey = settings.TOK_APIKEY
secretkey = settings.TOK_SECRETKEY
opentok = OpenTok(APIKey, secretkey)


class LivestreamSerializer(serializers.ModelSerializer):
    livestream_id = serializers.SerializerMethodField('get_id')
    user_id = serializers.SerializerMethodField('get_user')
    event_id = serializers.SerializerMethodField('get_event')
    username = serializers.SerializerMethodField()
    views = serializers.SerializerMethodField()

    class Meta:
        model = Livestream
        fields = ('livestream_id',
                  'user_id',
                  'event_id',
                  'archive',
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

    def get_views(self, obj):
        return Viewer.objects.filter(livestream=obj.pk).count()


class ViewerSerializer(serializers.ModelSerializer):
    user_id = serializers.SerializerMethodField('get_user')

    class Meta:
        model = Viewer
        fields = ('id',
                  'livestream_id',
                  'user_id',
                  'vote')

    def get_user(self, obj):
        return obj.user.pk


class ArchiveSerializer(serializers.ModelSerializer):

    class Meta:
        model = Archive
        fields = ('timestamp',
                  'video')
