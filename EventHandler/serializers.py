from rest_framework import serializers
from EventHandler.models import Event
from EventHandler.models import Category


class EventSerializer(serializers.ModelSerializer):
    event_id = serializers.SerializerMethodField('get_id')
    business_id = serializers.SerializerMethodField('get_company')
    category_id = serializers.SerializerMethodField('get_category')
    status = serializers.SerializerMethodField()
    start_date = serializers.DateTimeField()

    class Meta:
        model = Event
        fields = ('event_id',
                  'business_id',
                  'category_id',
                  'name',
                  'description',
                  'budget',
                  'image',
                  'location',
                  'start_date',
                  'end_date',
                  'status',)

    def get_id(self, obj):
        return obj.id

    def get_company(self, obj):
        return obj.company.pk

    def get_category(self, obj):
        return obj.category.pk

    def get_status(self, obj):
        return obj.self_status()


class CategorySerializer(serializers.ModelSerializer):
    category_id = serializers.SerializerMethodField('get_id')
    category_name = serializers.SerializerMethodField('get_name')

    class Meta:
        model = Category
        fields = ('category_id',
                  'category_name')

    def get_id(self, obj):
        return obj.id

    def get_name(self, obj):
        return obj.text
