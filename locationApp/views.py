from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from knox.auth import TokenAuthentication
from .serializers import *
from django.core.exceptions import ObjectDoesNotExist


# Create your views here.


class LocationWasteInformationView(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """
    authentication_classes = [TokenAuthentication, ]
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

        else :
            # location = LocationWasteInformation.objects.get(user_idx = request.user.idx)
            serializer = LocationWasteInformationSerializer(user.location_idx)
            return Response({
                "location_waste_information": serializer.data
            })

    # try:
        #
        #     location = LocationWasteInformation.objects.get(user_idx = request.user.idx)
        #     serializer = LocationWasteInformationSerializer(location)
        #     return Response({
        #         "location_waste_information": serializer.data
        #     })
        # except LocationWasteInformation.DoesNotExist:
        #     msg = "주소 관련 정보가 없습니다. 주소를 설정해주세요."
        #     return Response({
        #         "msg" : msg
        #     })


    # def put(self, request, format=None):
    #     serializer = LocationWasteInformationSerializer(request.user, data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #
    # def delete(self, request):
    #
    #     request.user.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)