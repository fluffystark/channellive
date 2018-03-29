from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from user_profile.models import Business


class BusinessSerializer(serializers.ModelSerializer):
    business_id = serializers.SerializerMethodField('get_id')
    user_id = serializers.SerializerMethodField('get_user')
    business_name = serializers.SerializerMethodField('get_name')

    class Meta:
        model = Business
        fields = ('business_id',
                  'user_id',
                  'business_name',)

    def get_id(self, obj):
        return obj.id

    def get_user(self, obj):
        return obj.user.pk

    def get_name(self, obj):
        return obj.company_name


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
    livestream_count = serializers.SerializerMethodField()
    award_count = serializers.SerializerMethodField()
    profile_pic = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('username',
                  'fullname',
                  'livestream_count',
                  'award_count',
                  'profile_pic')

    def get_fullname(self, obj):
        return obj.first_name + " " + obj.last_name

    def get_livestream_count(self, obj):
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
