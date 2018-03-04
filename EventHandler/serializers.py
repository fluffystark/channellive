from rest_framework import serializers
from EventHandler.models import Event


class EventSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = ('name',
                  'description',
                  'budget',
                  'image',
                  'location',
                  'company',
                  'category',
                  'start_date',
                  'end_date',)
