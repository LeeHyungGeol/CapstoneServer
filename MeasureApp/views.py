from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import *
from .serializers import *
from rest_framework import status
from django.http import Http404
from rest_framework import permissions
from .ar_markers.bin import ar_markers_generate
from .object_size import measure_length

# Create your views here.
class MarkerAPIView(APIView):

    permission_classes = [
        permissions.IsAuthenticated,
    ]


    def get(self, request, format=None):

        url = ar_markers_generate.generate_marker()
        return Response({
            "marker " : url
        })


class MeasureAPIView(APIView):

    permission_classes = [
        permissions.IsAuthenticated,
    ]


    def post(self, request, format=None):

        upload_serializer = MeasureUploadSerializer(data= request.data)

        if upload_serializer.is_valid():
            upload_serializer.save()
            img_url = upload_serializer.data['image']
            result_list = measure_length(img_url, request.user)

            if result_list is False:
                msg = "마커 인식에 실패했습니다."
                return Response({
                    "measure": {"code": 101,
                                        "msg" : msg}
                })
            elif len(result_list) == 0:
                msg = "길이 측정에 실패했습니다."
                return Response({
                    "measure": {"code": 102,
                                        "msg" : msg}
                })
            else :

                serializer = MeasureHistorySerializer(result_list, many=True)
                return Response({
                    "measure" :serializer.data
                }, status=status.HTTP_201_CREATED)
        return Response(upload_serializer.errors, status=status.HTTP_400_BAD_REQUEST)