from rest_framework import serializers
from file_upload.models import Image


class FileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Image
        fields = ('file',
                  'event')
