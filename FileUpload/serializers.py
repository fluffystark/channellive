from rest_framework import serializers
from FileUpload.models import EventImage


class FileSerializer(serializers.ModelSerializer):

    class Meta:
        model = EventImage
        fields = ('file',
                  'event')
