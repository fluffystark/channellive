from rest_framework import serializers
from EventHandler.models import Event
from UserProfile.serializers import BusinessSerializer


class EventSerializer(serializers.HyperlinkedModelSerializer):
    company = BusinessSerializer()

    class Meta:
        model = Event
        fields = ('name', 'description', 'budget', 'image', 'company')
