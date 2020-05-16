from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from .serializers import *
from django.core.exceptions import ObjectDoesNotExist


# Create your views here.


class UpdateLocationView(APIView):

    permission_classes = [
        permissions.IsAuthenticated,
    ]

    def post(self, request, format=None):
        user = request.user
        location_dong = request.data.get('dong')
        information = Community.objects.get(dong = location_dong)
        user.location_idx = information
        user.save()

        return Response(status=status.HTTP_201_CREATED)


class LocationWasteInformationView(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    def get(self, request, format=None):
        user = request.user
        if user.location_idx is None:
            msg = "주소 관련 정보가 없습니다. 주소를 설정해주세요."
            return Response({
                "msg" : msg
            })

        else:
            serializer = LocationWasteInformationSerializer(user.location_idx)
            return Response({
                "location_waste_information": serializer.data
            })


