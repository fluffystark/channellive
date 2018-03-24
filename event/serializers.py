from dateutil.parser import parse
from rest_framework import serializers
from event.models import Event
from event.models import Category


class EventSerializer(serializers.ModelSerializer):
    event_id = serializers.SerializerMethodField('get_id')
    business_id = serializers.SerializerMethodField('get_business')
    category_id = serializers.SerializerMethodField('get_category')
    status = serializers.SerializerMethodField()
    start_date = serializers.SerializerMethodField()
    end_date = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    review = serializers.SerializerMethodField()

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
                  'review',
                  'status',)

    def get_id(self, obj):
        return obj.id

    def get_business(self, obj):
        return obj.business.pk

    def get_category(self, obj):
        return obj.category.pk

    def get_status(self, obj):
        return obj.self_status()

    def get_start_date(self, obj):
        ret = parse(str(obj.start_date))
        ret = {"year": ret.year,
               "month": ret.month - 1,
               "dayOfMonth": ret.day,
               "hourOfDay": ret.hour,
               "minute": ret.minute,
               }
        return ret

    def get_end_date(self, obj):
        ret = parse(str(obj.end_date))
        ret = {"year": ret.year,
               "month": ret.month - 1,
               "dayOfMonth": ret.day,
               "hourOfDay": ret.hour,
               "minute": ret.minute,
               }
        return ret

    def get_image(self, obj):
        return obj.image.file.url

    def get_review(self, obj):
        return obj.get_review_display()


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
