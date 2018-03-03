from rest_framework import serializers


class TokSerializer(serializers.HyperlinkedModelSerializer):
    session_id = serializers.CharField()

