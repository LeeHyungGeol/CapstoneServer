from django.shortcuts import render
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import *
from .serializers import *
from rest_framework import status
from django.http import Http404
from rest_framework import permissions


# Create your views here.

class AllMessageListAPIVIEW(APIView):

    permission_classes = [
        permissions.IsAuthenticated,
    ]

    def get(self, request):
        user =request.user
        serializer = UserMessageSerializer(user)

        return Response({

           "message_list":serializer.data

        })


class MessageListAPIView(APIView):

    permission_classes = [
        permissions.IsAuthenticated,
    ]

    def get(self, request, user_id):
        user =request.user
        other_user = User.object.get(user_id = user_id)
        send_list = MessageSender.objects.filter(send_idx = user, recv_idx = other_user).order_by('send_date')
        send_serializer = MessageSenderSerializer(send_list, many=True)

        receive_list = MessageReceiver.objects.filter(recv_idx =user, send_idx = other_user).order_by('send_date')
        recv_serializer = MessageReceiverSerializer(receive_list, many=True)
        return Response({

            "send_list": send_serializer.data,
            "recv_list" : recv_serializer.data

        })


    def delete(self, request, user_id):
        user =request.user
        other_user = User.object.get(user_id = user_id)
        send_list = MessageSender.objects.filter(send_idx = user, recv_idx = other_user).order_by('send_date')
        send_list.delete()

        receive_list = MessageReceiver.objects.filter(recv_idx =user, send_idx = other_user).order_by('send_date')
        receive_list.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

    def post(self, request, user_id):
        sender = request.user
        receiver = User.object.get(user_id = user_id)
        message = MessageSender.objects.create(send_idx =sender, recv_idx = receiver, recv_chk = 0 )
        serializer_send = MessageSenderSerializer(message, data=request.data)

        message = MessageReceiver.objects.create(send_idx =sender, recv_idx = receiver)
        serializer_recv = MessageReceiverSerializer(message, data=request.data)

        if serializer_send.is_valid() and serializer_recv.is_valid():
            serializer_send.save()
            serializer_recv.save()
            return Response({
                "message" : serializer_send.data,

            },status=status.HTTP_201_CREATED)
        return Response(serializer_send.errors, status=status.HTTP_400_BAD_REQUEST)




class MessageDetailAPIView(APIView):

    permission_classes = [
        permissions.IsAuthenticated,
    ]

    def get_object(self, message_idx):
        try:
            return MessageSender.objects.get(idx=message_idx)
        except MessageSender.DoesNotExist:
            raise Http404

    def get(self, request, message_idx, format=None):
        message = self.get_object(message_idx)
        message.recv_chk = 1
        message.save()
        serializer = MessageSenderSerializer(message)
        return Response({"message": serializer.data})

    def delete(self, request, message_idx):

        msg = MessageReceiver.objects.get(idx = message_idx)
        msg.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)