from rest_framework import serializers
from FileUpload.models import EventImage


class FileSerializer(serializers.ModelSerializer):
    event_id = serializers.SerializerMethodField()

    class Meta:
        model = EventImage
        fields = ('file',
                  'event_id')

    def get_event_id(self, obj):
        return obj.event.id
