from rest_framework import serializers
from EventHandler.models import Event


class EventSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = ('id',
                  'company',
                  'category',
                  'name',
                  'description',
                  'budget',
                  'image',
                  'location',
                  'start_date',
                  'end_date',)
