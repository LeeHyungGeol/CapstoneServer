from rest_framework import serializers
from .models import *
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
    class Meta:
        model = User
        fields = ("user_id", "user_nm", 'location_idx', 'point')
