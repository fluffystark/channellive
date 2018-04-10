from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from user_profile.models import Business


class BusinessSerializer(serializers.ModelSerializer):
    business_id = serializers.SerializerMethodField('get_id')
    user_id = serializers.SerializerMethodField('get_user')
    business_name = serializers.SerializerMethodField('get_name')
    incoming_count = serializers.SerializerMethodField()
    ongoing_count = serializers.SerializerMethodField()
    ended_count = serializers.SerializerMethodField()

    class Meta:
        model = Business
        fields = ('business_id',
                  'user_id',
                  'business_name',
                  'incoming_count',
                  'ongoing_count',
                  'ended_count')

    def get_id(self, obj):
        return obj.id

    def get_user(self, obj):
        return obj.user.pk

    def get_name(self, obj):
        return obj.company_name

    def get_incoming_count(self, obj):
        return obj.events.filter(status=1).count()

    def get_ongoing_count(self, obj):
        return obj.events.filter(status=2).count()

    def get_ended_count(self, obj):
        return obj.events.filter(status=3).count()


class UserRegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True,
                                   validators=[UniqueValidator(queryset=User.objects.all())])

    class Meta:
        model = User
        fields = ('username',
                  'password',
                  'first_name',
                  'last_name',
                  'email',)

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class UserSerializer(serializers.ModelSerializer):
    fullname = serializers.SerializerMethodField()
    video_count = serializers.SerializerMethodField()
    award_count = serializers.SerializerMethodField()
    profile_pic = serializers.SerializerMethodField()
    gold_count = serializers.SerializerMethodField()
    silver_count = serializers.SerializerMethodField()
    bronze_count = serializers.SerializerMethodField()
    total_likes = serializers.SerializerMethodField()
    total_views = serializers.SerializerMethodField()
    bio = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('username',
                  'fullname',
                  'email',
                  'video_count',
                  'award_count',
                  'profile_pic',
                  'total_likes',
                  'total_views',
                  'gold_count',
                  'silver_count',
                  'bronze_count',
                  'bio',)

    def get_fullname(self, obj):
        return obj.first_name + " " + obj.last_name

    def get_video_count(self, obj):
        return obj.livestreams.all().count()

    def get_profile_pic(self, obj):
        ret = None
        if obj.userprofile.profilepic == "":
            ret = "/media/default/avatar.png"
        else:
            ret = obj.userprofile.profilepic.url
        return ret

    def get_award_count(self, obj):
        return obj.prizes.all().count()

    def get_gold_count(self, obj):
        return obj.prizes.filter(title="First Prize").count()

    def get_silver_count(self, obj):
        return obj.prizes.filter(title="Second Prize").count()

    def get_bronze_count(self, obj):
        return obj.prizes.filter(title="Third Prize").count()

    def get_total_likes(self, obj):
        livestreams = obj.livestreams.all()
        likes = 0
        for livestream in livestreams:
            likes += livestream.votes
        return likes

    def get_total_views(self, obj):
        livestreams = obj.livestreams.all()
        views = 0
        for livestream in livestreams:
            views += livestream.viewers.all().count()
        return views

    def get_bio(self, obj):
        return obj.userprofile.bio


class ChangePasswordSerializer(serializers.ModelSerializer):
    user_id = serializers.SerializerMethodField('get_user')

    class Meta:
        model = User
        fields = ('new_password',)

    def get_user(self, obj):
        return obj.pk

    def update(self, instance, validated_data):
        password = validated_data.get('password')
        instance.set_password(password)
        instance.save()
