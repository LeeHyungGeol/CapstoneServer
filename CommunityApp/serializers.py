from rest_framework import serializers
from .models import *


class CommunityListSerializer(serializers.ModelSerializer):
    user_id =serializers.CharField(source='user_idx.user_id')
    class Meta:
        model = Community
        fields = ('idx', 'title', 'date',  'share_complete', 'user_id')
        read_only_fields = ['idx']


class CommunityDetailSerializer(serializers.ModelSerializer):
    user_id = serializers.CharField(source='user_idx.user_id', required=False)

    class Meta:
        model = Community
        exclude = ['user_idx']
        read_only_fields = ['idx']