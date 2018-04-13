from dateutil.parser import parse
from rest_framework import serializers
from event.models import Event
from event.models import Category
from event.models import Prize
from event.models import Bookmark
from OpenTokHandler.models import Livestream


class EventSerializer(serializers.ModelSerializer):
    event_id = serializers.SerializerMethodField('get_id')
    business_id = serializers.SerializerMethodField('get_business')
    business_name = serializers.SerializerMethodField()
    category_id = serializers.SerializerMethodField('get_category')
    start_date = serializers.SerializerMethodField()
    end_date = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    review = serializers.SerializerMethodField()
    is_bookmarked = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = ('event_id',
                  'business_id',
                  'business_name',
                  'category_id',
                  'name',
                  'description',
                  'budget',
                  'image',
                  'location',
                  'start_date',
                  'end_date',
                  'review',
                  'status',
                  'is_bookmarked',)

    def get_description(self, obj):
        description = obj.description
        if 'check_user' in self.context.keys():
            user = self.context['check_user']
            prize = obj.prizes.filter(user=user).first()
            description = prize.title
        return description

    def get_is_bookmarked(self, obj):
        is_bookmarked = False
        if 'user' in self.context.keys():
            user = self.context['user']
            bookmark = obj.bookmarks.filter(user=user).first()
            if bookmark is not None:
                is_bookmarked = bookmark.is_bookmarked
        return is_bookmarked

    def get_business_name(self, obj):
        return obj.business.company_name

    def get_id(self, obj):
        return obj.id

    def get_business(self, obj):
        return obj.business.pk

    def get_category(self, obj):
        return obj.category.pk

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
        ret = None
        if obj.image == "":
            ret = "http://yuchipashe.me:8000/media/default/default_event.jpg"
        else:
            ret = obj.image.url
        return ret

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


class PrizeSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    livestream_id = serializers.SerializerMethodField()
    user_id = serializers.SerializerMethodField()

    class Meta:
        model = Prize
        fields = ('username',
                  'user_id',
                  'title',
                  'livestream_id',)

    def get_username(self, obj):
        user = -1
        if obj.user is not None:
            user = obj.user.username
        return user

    def get_user_id(self, obj):
        user_id = -1
        if obj.user is not None:
            user_id = obj.user.pk
        return user_id

    def get_livestream_id(self, obj):
        livestream = Livestream.objects.filter(event=obj.event,
                                               user=obj.user).first()
        if livestream is not None:
            return livestream.id
        return -1


class EventDisplaySerializer(serializers.Serializer):

    class Meta:
        model = Event
        fields = ('name',
                  'description',
                  'category',
                  'budget',
                  'start_date',
                  'end_date',
                  'verification_uuid')


class EventBookmarkSerializer(serializers.Serializer):

    class Meta:
        model = Bookmark
        fields = ('user',
                  'event',)
