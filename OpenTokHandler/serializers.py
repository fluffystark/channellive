from rest_framework import serializers


class TokSerializer(serializers.Serializer):
    session_id = serializers.CharField()

    class Meta:
        fields = ('session_id')
