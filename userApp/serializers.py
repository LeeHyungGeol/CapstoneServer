from rest_framework import serializers
from .models import *
from CommunityApp.models import Community
from django.contrib.auth import authenticate

# 회원가입
class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('idx', 'user_id', 'password')
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.object.create_user(
            validated_data["user_id"], validated_data["password"]
        )
        return user

# user 확인용
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('idx', 'user_id')


class UserProfileSerializer(serializers.ModelSerializer):
    location_name = serializers.CharField(source='location_idx.dong')
    class Meta:
        model = User
        fields = ("user_id", "user_nm", 'location_name', 'point')


class UpdateUserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("user_id", "user_nm")



class UserShareCompleteCheckSerializer(serializers.ModelSerializer):
    class Meta:
        model = Community
        fields = ("idx", "title", "content", 'date', 'share_complete'
                  , 'user_idx')
