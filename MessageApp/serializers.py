from rest_framework import serializers
from .models import *


class MessageSenderSerializer(serializers.ModelSerializer):
    sender_id = serializers.CharField(source='send_idx.user_id', required=False)
    receiver_id = serializers.CharField(source='recv_idx.user_id', required=False)
    class Meta:
        model = MessageSender
        fields = '__all__'
        ordering = ['date']


class MessageReceiverSerializer(serializers.ModelSerializer):
    sender_id = serializers.CharField(source='send_idx.user_id', required=False)
    receiver_id = serializers.CharField(source='recv_idx.user_id', required=False)
    class Meta:
        model = MessageReceiver
        fields = '__all__'
        ordering = ['date']


class UserMessageSerializer(serializers.ModelSerializer):
    send_message = MessageSenderSerializer(source='sender_send_set', many=True)
    recv_message = MessageReceiverSerializer(source='receiver_recv_set', many=True)

    class Meta:
        model = User
        fields = ['send_message', 'recv_message']
